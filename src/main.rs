use clap::Parser;
use reqwest;
use dotenv;
use core::option::Option;
use tokio;
use futures::{stream, StreamExt};
use std::time::Instant;

const CONCURRENT_REQUESTS: usize = 100;

#[derive(Parser)]
#[command(name="weather")]
#[command(about="Weather in the terminal",long_about = None)]

struct Args{
    ///Number of days for the forecast
    #[arg(short,default_value_t = 0)]
    days:u8,
}

#[tokio::main]
async fn main() {
    
    dotenv::from_filename(".env").unwrap();

    let mut api_key: Option<String> = None;
    for(key,value) in std::env::vars(){
        if key != "APIKEY"{
            continue;
        }
        api_key=Some(value)
    }

    if api_key.is_none(){
        panic!("need API Key");
    }
    let api_key = api_key.unwrap();

    // let args: Args = Args::parse();

    let client = reqwest::Client::new();
    let urls = vec!["http://localhost:5000/get_weather?city=London"; CONCURRENT_REQUESTS];
    // let url = format!("http://localhost:6969/get_weather?city=London");

    
    let bodies = stream::iter(urls)
        .map(|url| {
            let client = &client;
            async move {
                let start_time = Instant::now(); // Record the start time
                let resp = client.get(url).send().await?;
                let end_time = Instant::now(); // Record the start time
                let response_time = end_time.duration_since(start_time); // Calculate the response time
                println!("Response time for {}: {:?}", url, response_time);
                resp.bytes().await
            }
        })
        .buffer_unordered(CONCURRENT_REQUESTS);



    bodies
        .for_each(|body| async move {
            println!("body = {:?}", body);
        })
        .await;
    // let body = reqwest::blocking::get(url)?
    // .text()?;

    // println!("body = {:?}", body);
    //println!("{}",args.days);
    // Ok(())
}
