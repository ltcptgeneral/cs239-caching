# Tests latency and hit rate of endpoints. Can be configured with weighted averages for various endpoints.

import requests
import random
import json
from tqdm import tqdm
import time

baseurl = "http://localhost:8000"

chance_of_selecting_friend = 0.7

user_friends = json.loads(requests.get(baseurl + "/users_and_friends").content)
user_ids = json.loads(requests.get(baseurl + "/users").content)["ids"]

random.seed(0)

def fetch_friend(prob):
    return random.random() < prob

def generate_random():
    random_user = str(random.choice(user_ids))
    return random_user

def generate_random_friend(user):
    next_user = str(random.choice(user_friends[user]))
    return next_user

times = []
hits = []

start = time.time()
curr_user = generate_random()
for i in tqdm(range(10000)):
    url = baseurl + "/user/" + curr_user
    response = requests.get(url)
    content = json.loads(response.content)
    times.append(content["time_ms"])
    hits.append(content["source"] == "cache")
    if fetch_friend(chance_of_selecting_friend):
        curr_user = generate_random_friend(curr_user)
    else:
        curr_user = generate_random()
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