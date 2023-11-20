# POPL_Assignment
A comparative study between Rust &amp; C++ on concurrency, performance &amp; parsing using a locally hosted gunicorn API server

Problem Statement:
Weather forecasting applications often need to make multiple API
requests concurrently to fetch both current and forecast data for different locations. C++ can be
challenging when writing concurrent code due to potential data races. Rust's ownership model
enforces safe concurrency, helping developers avoid data race issues and simplifying parallel
API requests.
We will be drawing a comparison between the fetch time of a http request first from a client
written in Rust and then in C++.We will see their variation as we change the number of workers and other 
parameters.The server is hosted locally and the backend code of the same is written in python.

Software architecture:
For benchmarking the http server,we are using apache benchmark.

 POPL Aspects: 

 Results:

 Potential for future work:

