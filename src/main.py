import requests
import time
import threading
import dotenv
import os

# Load API key from .env file
dotenv.load_dotenv()
api_key = os.getenv('API_KEY')

def get_request():
    start = time.time()

    # Request to API endpoint
    response = requests.get('http://localhost:5000/get_weather?city=London&api_key=' + api_key)

    end = time.time()
    print(response.json())
    print(str((end - start) * 1000) + ' ms')

threads = []
for i in range(20):
    t = threading.Thread(target=get_request)
    threads.append(t)
    t.start()

for t in threads:
    t.join()