# Tests latency and hit rate of endpoints. Can be configured with weighted averages for various endpoints.

import requests
import random
import json
from tqdm import tqdm
import time

baseurl = "http://localhost:8000"

endpoints = {
    "/user/{user_id}": 1
}

user_ids = json.loads(requests.get(baseurl + "/users").content)["ids"]

random.seed(0)

def generate_random():
    x = random.choices(list(endpoints.keys()), list(endpoints.values()))[0] # select randomly from endpoint (keys) with weight (values)

    random_user = str(random.choice(user_ids))
    x = x.replace("{user_id}", random_user)

    return baseurl + x

times = []
hits = []

start = time.time()
for i in tqdm(range(10000)):
    url = generate_random()
    response = requests.get(url)
    content = json.loads(response.content)
    times.append(content["time_ms"])
    hits.append(content["source"] == "cache")
end = time.time()

hits_count = sum(hits)
miss_count = len(hits) - hits_count

hits_time = 0
miss_time = 0
for i in range(len(times)):
    if hits[i]:
        hits_time += times[i]
    else:
        miss_time += times[i]
total_time = hits_time + miss_time

print(f"hits: {hits_count} misses: {miss_count} ratio: { hits_count / (hits_count + miss_count)}")
print(f"average response time (ms)           : {total_time / len(times)}")
print(f"average cache hit response time (ms) : {hits_time / hits_count}")
print(f"average cache miss response time (ms): {miss_time / miss_count}")
print(f"cache throughput (requests / ms)     : { len(times) / total_time}")
print(f"real throughput  (requests / ms)     : { len(times) / (end - start) / 1000}")