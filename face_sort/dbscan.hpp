#pragma once
#include <vector>
#include <cmath>
#include <algorithm>

// Simple DBSCAN implementation

template <typename T>
class DBSCAN {
public:
    DBSCAN(T eps, int minPts) : eps(eps), minPts(minPts) {}

    std::vector<int> fit(const std::vector<std::vector<T>>& data) {
        int n = data.size();
        std::vector<int> labels(n, UNCLASSIFIED);
        int clusterId = 0;
        for (int i = 0; i < n; ++i) {
            if (labels[i] == UNCLASSIFIED) {
                if (expandCluster(data, i, clusterId, labels)) {
                    clusterId++;
                }
            }
        }
        return labels;
    }

private:
    const int UNCLASSIFIED = -2;
    const int NOISE = -1;
    T eps;
    int minPts;

    static T distance(const std::vector<T>& a, const std::vector<T>& b) {
        T dist = 0;
        for (size_t i = 0; i < a.size(); ++i) {
            T diff = a[i] - b[i];
            dist += diff * diff;
        }
        return std::sqrt(dist);
    }

    std::vector<int> regionQuery(const std::vector<std::vector<T>>& data, int idx) {
        std::vector<int> neighbors;
        for (int i = 0; i < (int)data.size(); ++i) {
            if (distance(data[idx], data[i]) <= eps) {
                neighbors.push_back(i);
            }
        }
        return neighbors;
    }

    bool expandCluster(const std::vector<std::vector<T>>& data, int idx, int clusterId, std::vector<int>& labels) {
        auto neighbors = regionQuery(data, idx);
        if ((int)neighbors.size() < minPts) {
            labels[idx] = NOISE;
            return false;
        }
        for (int nIdx : neighbors)
            labels[nIdx] = clusterId;
        // Copy neighbors to avoid modifying while iterating
        std::vector<int> toProcess = neighbors;
        while (!toProcess.empty()) {
            int current = toProcess.back();
            toProcess.pop_back();
            auto currentNeighbors = regionQuery(data, current);
            if ((int)currentNeighbors.size() >= minPts) {
                for (int nIdx : currentNeighbors) {
                    if (labels[nIdx] == UNCLASSIFIED || labels[nIdx] == NOISE) {
                        if (labels[nIdx] == UNCLASSIFIED)
                            toProcess.push_back(nIdx);
                        labels[nIdx] = clusterId;
                    }
                }
            }
        }
        return true;
    }
};
