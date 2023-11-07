import requests
import time
import threading

def get_request():
    start = time.time()
    r = requests.get('http://localhost:5000/get_weather?city=London')
    end = time.time()
    print(end - start)

threads = []
for i in range(100):
    t = threading.Thread(target=get_request)
    threads.append(t)
    t.start()

for t in threads:
    t.join()