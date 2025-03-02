# Tests latency and hit rate of endpoints. Can be configured with weighted averages for various endpoints.

import requests
import random
import json
from tqdm import tqdm
import time
from utils import print_report

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

print_report(hits, times, end - start)