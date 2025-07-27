#include <filesystem>
#include <iostream>
#include <map>
#include <set>
#include <vector>
#include <string>

// Dlib headers
#include <dlib/dnn.h>
#include <dlib/image_processing/frontal_face_detector.h>
#include <dlib/image_processing.h>
#include <dlib/image_io.h>
#include <dlib/opencv.h>

// OpenCV
#include <opencv2/opencv.hpp>

// Your DBSCAN header
#include "dbscan.hpp"

namespace fs = std::filesystem;

// ----------------------------------------------------------------------------------------
// The face-recognition ResNet (from dlib/examples/dnn_face_recognition_ex.cpp)
namespace dlib {

// Define residual blocks
template <template<int,template<typename>class,int,typename> class block,
          int N, template<typename>class BN, typename SUBNET>
using residual = add_prev1<block<N,BN,1,tag1<SUBNET>>>;

template <template<int,template<typename>class,int,typename> class block,
          int N, template<typename>class BN, typename SUBNET>
using residual_down = add_prev2<avg_pool<2,2,2,2,skip1<tag2<block<N,BN,2,tag1<SUBNET>>>>>>;

template <int N, template<typename> class BN, int stride, typename SUBNET>
using block  = BN<con<N,3,3,1,1,relu<BN<con<N,3,3,stride,stride,SUBNET>>>>>;

template <int N, typename SUBNET> using ares      = relu<residual<block,N,affine,SUBNET>>;
template <int N, typename SUBNET> using ares_down = relu<residual_down<block,N,affine,SUBNET>>;

template <typename SUBNET> using alevel0 = ares_down<256,SUBNET>;
template <typename SUBNET> using alevel1 = ares<256,ares<256,ares_down<256,SUBNET>>>;
template <typename SUBNET> using alevel2 = ares<128,ares<128,ares_down<128,SUBNET>>>;
template <typename SUBNET> using alevel3 = ares<64,ares<64,ares<64,ares_down<64,SUBNET>>>>;
template <typename SUBNET> using alevel4 = ares<32,ares<32,ares<32,SUBNET>>>;

using anet_type = loss_metric<fc_no_bias<128,avg_pool_everything<
                            alevel0<
                            alevel1<
                            alevel2<
                            alevel3<
                            alevel4<
                            max_pool<3,3,2,2,relu<affine<con<32,7,7,2,2,
                            input_rgb_image_sized<150>
                            >>>>>>>>>>>>;
} // namespace dlib
// ----------------------------------------------------------------------------------------

//------------------ Utilities ------------------//

std::vector<dlib::matrix<dlib::rgb_pixel>> load_image_faces(
    const fs::path& img_path,
    dlib::frontal_face_detector& detector,
    dlib::shape_predictor& sp)
{
    cv::Mat cv_img = cv::imread(img_path.string());
    cv::Mat rgb;
    cv::cvtColor(cv_img, rgb, cv::COLOR_BGR2RGB);
    dlib::matrix<dlib::rgb_pixel> dlib_img;
    dlib::assign_image(dlib_img, dlib::cv_image<dlib::rgb_pixel>(rgb));

    auto dets = detector(dlib_img);
    std::vector<dlib::matrix<dlib::rgb_pixel>> faces;
    for (auto& r : dets) {
        auto shape = sp(dlib_img, r);
        dlib::matrix<dlib::rgb_pixel> face;
        extract_image_chip(dlib_img,
                           get_face_chip_details(shape,150,0.25),
                           face);
        faces.push_back(face);
    }
    return faces;
}

std::vector<dlib::matrix<dlib::rgb_pixel>> load_video_faces(
    const fs::path& vid_path,
    dlib::frontal_face_detector& detector,
    dlib::shape_predictor& sp,
    int frameStep = 30)
{
    cv::VideoCapture cap(vid_path.string());
    std::vector<dlib::matrix<dlib::rgb_pixel>> faces;
    cv::Mat frame;
    int idx = 0;
    while (cap.read(frame)) {
        if (idx % frameStep == 0) {
            cv::Mat rgb;
            cv::cvtColor(frame, rgb, cv::COLOR_BGR2RGB);
            dlib::matrix<dlib::rgb_pixel> dimg;
            dlib::assign_image(dimg, dlib::cv_image<dlib::rgb_pixel>(rgb));
            auto dets = detector(dimg);
            for (auto& r : dets) {
                auto shape = sp(dimg, r);
                dlib::matrix<dlib::rgb_pixel> face;
                extract_image_chip(dimg,
                                   get_face_chip_details(shape,150,0.25),
                                   face);
                faces.push_back(face);
            }
        }
        ++idx;
    }
    return faces;
}

int main(int argc, char** argv) {
    if (argc < 2) {
        std::cerr << "Usage: " << argv[0] << " <root_folder>\n";
        return 1;
    }
    fs::path root = argv[1];

    auto detector = dlib::get_frontal_face_detector();
    dlib::shape_predictor sp;
    dlib::deserialize("shape_predictor_5_face_landmarks.dat") >> sp;
    dlib::anet_type net;
    dlib::deserialize("dlib_face_recognition_resnet_model_v1.dat") >> net;

    std::vector<dlib::matrix<float,0,1>> embeddings;
    std::vector<std::string> files;

    for (auto& p : fs::recursive_directory_iterator(root)) {
        if (!p.is_regular_file()) continue;
        auto ext = p.path().extension().string();
        if (ext == ".jpg" || ext == ".jpeg" || ext == ".png") {
            auto faces = load_image_faces(p.path(), detector, sp);
            for (auto& f : faces) {
                embeddings.push_back(net(f));
                files.push_back(p.path().string());
            }
        } else if (ext == ".mp4" || ext == ".avi" || ext == ".mkv") {
            auto faces = load_video_faces(p.path(), detector, sp);
            for (auto& f : faces) {
                embeddings.push_back(net(f));
                files.push_back(p.path().string());
            }
        }
    }

    if (embeddings.empty()) {
        std::cout << "No faces found.\n";
        return 0;
    }

    std::vector<std::vector<float>> data;
    for (auto& v : embeddings)
        data.emplace_back(v.begin(), v.end());
    DBSCAN<float> db(0.6f, 3);
    auto labels = db.fit(data);

    std::map<int,std::set<std::string>> report;
    for (size_t i = 0; i < labels.size(); ++i)
        report[labels[i]].insert(files[i]);

    for (auto& [lbl, paths] : report) {
        std::cout << (lbl < 0 ? "unknown" : "person_" + std::to_string(lbl)) << ":\n";
        for (auto& f : paths)
            std::cout << "  " << f << "\n";
    }
    return 0;
}
