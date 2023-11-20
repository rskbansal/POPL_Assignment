#include <iostream>
#include <httplib.h>
#include <nlohmann/json.hpp>

const std::string BASE_URL = "http://127.0.0.1:5000/get_weather?city=London";
const int CONCURRENT_REQUESTS = 100;

int main() {
    httplib::Client client(BASE_URL.c_str());

    std::vector<std::string> urls(CONCURRENT_REQUESTS, BASE_URL);

    for (const auto& url : urls) {
        auto start_time = std::chrono::high_resolution_clock::now();

        auto response = client.Get(url.c_str());

        auto end_time = std::chrono::high_resolution_clock::now();
        auto response_time = std::chrono::duration_cast<std::chrono::milliseconds>(end_time - start_time);

        if (response) {
            std::cout << "Response time for " << url << ": " << response_time.count() << " ms\n";
            std::cout << "Body: " << response->body << "\n";
        } else {
            std::cerr << "Request failed for " << url << "\n";
        }
    }

    return 0;
}