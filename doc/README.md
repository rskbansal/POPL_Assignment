# POPL_Assignment
A comparative study between Rust &amp; C++ on concurrency, performance &amp; parsing using a locally hosted gunicorn API server

![Concurrency](/doc/concurrency.webp)

## Problem Statement:
- Weather forecasting applications often need to make multiple API
- Requests concurrently to fetch both current and forecast data for different locations
- C++ can be challenging when writing concurrent code due to potential data races
- Rust's ownership model enforces safe concurrency, helping developers avoid data race issues and simplifying parallel API requests
- We will be drawing a comparison between the fetch time of a http request first from a client written in Rust and then in C++
- We will see their variation as we change the number of workers and other parameters
- The server is hosted locally and the backend code of the same is written in python


## Software architecture:
- For benchmarking the HTTP server, we are using Apache Benchmark
- Gunicorn is used as the python API server. It allows user to run any Python application concurrently by running multiple Python processes within a single dyno. It provides a perfect balance of performance, flexibility, and configuration simplicity
- Cargo: Build System and Package Manager
- Build System: Cargo acts as the build system for Rust projects. It automates the build process, compiling code, managing dependencies, and handling various tasks related to building and packaging Rust applications.
- Package Manager: Cargo is also the package manager for Rust. It allows developers to easily manage dependencies, download and install packages, and publish their own packages to the crates.io registry.


## POPL Aspects: 
- Ownership: The client owns the reqwest::Client instance.
- Borrowing: The closure inside the map function borrows client and url using move and &, respectively.

1. Concurrent Requets (Rust):
```rust
let client = reqwest::Client::new();
let urls = vec!["http://localhost:5000/get_weather?city=London"; CONCURRENT_REQUESTS];

let bodies = stream::iter(urls)
    .map(|url| async move {
        let start_time = Instant::now();
        let resp = client.get(url).send().await?;
        let end_time = Instant::now();
        let response_time = end_time.duration_since(start_time);
        println!("Response time for {}: {:?}", url, response_time);
        resp.bytes().await
    })
    .buffer_unordered(CONCURRENT_REQUESTS);
```

2. Asynchronous Programming (Rust):
```rust
let bodies = stream::iter(urls)
    .map(|url| async move {
        // ...
    })
    .buffer_unordered(CONCURRENT_REQUESTS);

bodies
    .for_each(|body| async move {
        // ...
    })
    .await;
```

- Asynchronous Programming: Utilizes the async/await syntax for asynchronous tasks.
- Futures and Streams: Leverages the futures library for working with asynchronous streams.

3. Explicit Error Handling (Rust):
```rust
let resp = client.get(url).send().await?;
```

- Result Type: Uses the Result type for explicit error handling, ensuring that errors are handled appropriately.

4. Concurrency with std::async (C++):
```cpp
std::vector<std::future<void>> futures;

for (const auto& url : urls) {
    futures.push_back(std::async(std::launch::async, [&client, url]() {
        // ...
    }));
}

std::for_each(futures.begin(), futures.end(), [](std::future<void>& f) {
    f.get();
});
```

- `std::async` : Creates asynchronous tasks using std::async.
- Futures and Concurrency: Uses std::future to represent asynchronous tasks and manages them with std::for_each.

## Results:
[PDF](./results/Results.pdf)


## Potential for Future Work:

### Additional Features:
- Consider adding additional features to the program, such as support for different APIs, error recovery mechanisms, or enhanced logging. This can help uncover language-specific challenges and strengths.

### Security Audits:
- Perform security audits to identify potential vulnerabilities in the code
- Consider aspects such as secure handling of API keys, protection against common web vulnerabilities, and adherence to best practices.

### Cross-Platform Considerations:
- Evaluate how well each language supports cross-platform development
- Ensure that the program works consistently across different operating systems and platforms.


## INSTALLATION

### API Server
```bash
pip install -r requirements.txt
cd code-orig/src
gunicorn -c gunicorn_config.py backend_api:app
```

### Apache Benchmark
```bash
sudo apt install apache2-utils
ab -n 20 -c 20 "http://localhost:5000/get_weather?city=Goa&api_key=p0pl-15-fun"
```

### Rust:
```bash
cd code-orig
cargo run
```

### C++:
- Download `httplib.h` from the following [repository](https://github.com/yhirose/cpp-httplib)
```bash
cd code-orig/src
g++ main.cpp
./a.out
```

### Python:
- The version of Python used is 3.11.5
```bash
pip install -r requirements.txt
cd code-orig/src
python main.py
```