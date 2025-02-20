# Tests latency and hit rate of endpoints. Can be configured with weighted averages for various endpoints.

import requests
import random
import json

baseurl = "http://localhost:8000"

endpoints = {
    "/user/{user_id}": 1
}

def generate_random():
    x = random.choices(list(endpoints.keys()), list(endpoints.values()))[0] # select randomly from endpoint (keys) with weight (values)

    random_user = str(random.randint(1, 3))
    x = x.replace("{user_id}", random_user)

    return baseurl + x

times = []
hits = []

for i in range(1000):
    url = generate_random()
    response = requests.get(url)
    content = json.loads(response.content)
    times.append(content["time_ms"])
    hits.append(content["source"] == "cache")

print(f"average response time (ms): {sum(times) / len(times)}")
print(f"hits: {sum(hits)} misses: {len(hits) - sum(hits)}")