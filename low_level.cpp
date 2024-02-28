#include <cpr/cpr.h>

#include <Eigen/Dense>
#include <iostream>
#include <nlohmann/json.hpp>

using json = nlohmann::json;

class Task {
public:
    std::string id;
    int size;
    float time;
    Eigen::MatrixXf a;
    Eigen::VectorXf b;
    Eigen::VectorXf x;

    Task(const json& j) :
        id(j.at("identifier").get<std::string>()),
        size(j.at("size").get<int>()),
        time(j.at("time").get<float>()),
        a(ConvertToEigenMatrix(j.at("a").get<std::vector<std::vector<float>>>())),
        b(Eigen::VectorXf::Map(j.at("b").get<std::vector<float>>().data(), size)),
        x(Eigen::VectorXf::Map(j.at("x").get<std::vector<float>>().data(), size)) {}

    void print() const {
        std::cout << "- id: " << id << std::endl;
        std::cout << "- a: \n" << a << "\n\n";
    }

    void work() {
        auto start = std::chrono::high_resolution_clock::now();
        x = a.colPivHouseholderQr().solve(b);
        auto end = std::chrono::high_resolution_clock::now();
        time = std::chrono::duration_cast<std::chrono::nanoseconds>(end - start).count() * 1e-9;
    }

    json toJson() const {
        return {
            {"identifier", id},
            {"size", size},
            {"time", time},
            {"a", ConvertToVector(a)},
            {"b", std::vector<float>(b.data(), b.data() + b.rows() * b.cols())},
            {"x", std::vector<float>(x.data(), x.data() + x.rows() * x.cols())}
        };
    }

private:
    static std::vector<std::vector<float>> ConvertToVector(const Eigen::MatrixXf& eMatrix) {
        std::vector<std::vector<float>> data(eMatrix.rows(), std::vector<float>(eMatrix.cols(), 0));

        for (int i = 0; i < eMatrix.rows(); ++i)
            for (int j = 0; j < eMatrix.cols(); ++j)
                data[i][j] = eMatrix(i, j);

        return data;
    }

    static Eigen::MatrixXf ConvertToEigenMatrix(const std::vector<std::vector<float>>& data) {
        Eigen::MatrixXf eMatrix(data.size(), data.front().size());
        for (int i = 0; i < data.size(); ++i)
            eMatrix.row(i) = Eigen::VectorXf::Map(data[i].data(), data.front().size());
        return eMatrix;
    }
};

int main() {
    while (true) {
        auto r = cpr::Get(cpr::Url{"http://localhost:8000"});
        if (r.status_code != 200) continue;

        json j = json::parse(r.text);
        Task task(j);
        std::cout << "Received task #" << task.id << std::endl;

        task.work();

        json response = task.toJson();
        std::cout << "Finished task #" << task.id << " in " << task.time << " seconds\n";

        auto r2 = cpr::Post(cpr::Url{"http://localhost:8000"}, cpr::Body{response.dump()},
                            cpr::Header{{"Content-Type", "application/json"}});
    }

    return 0;
}