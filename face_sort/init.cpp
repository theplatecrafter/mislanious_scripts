#include <iostream>
#include <fstream>
#include <cstdlib>
#include <vector>
#include <string>
#include <filesystem>

struct ModelInfo {
    std::string url;
    std::string filename;
};

int main() {
    std::vector<ModelInfo> models = {
        {"https://dlib.net/files/shape_predictor_5_face_landmarks.dat.bz2", "shape_predictor_5_face_landmarks.dat.bz2"},
        {"https://dlib.net/files/dlib_face_recognition_resnet_model_v1.dat.bz2", "dlib_face_recognition_resnet_model_v1.dat.bz2"}
    };

    for (auto &m : models) {
        if (!std::filesystem::exists(m.filename.substr(0, m.filename.size() - 4))) {
            std::string cmd = "wget " + m.url + " -O " + m.filename + " && bzip2 -dk " + m.filename;
            std::cout << "Downloading and extracting: " << m.url << std::endl;
            if (std::system(cmd.c_str()) != 0) {
                std::cerr << "Failed to download: " << m.url << std::endl;
                return 1;
            }
        } else {
            std::cout << "Already present: " << m.filename.substr(0, m.filename.size() - 4) << std::endl;
        }
    }

    std::cout << "All model files are ready." << std::endl;
    return 0;
}
