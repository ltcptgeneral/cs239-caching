# Tests latency and hit rate of endpoints. Can be configured with weighted averages for various endpoints.

import requests
import random
import json
from tqdm import tqdm
import time
from utils import print_report

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

print_report(hits, times, end - start)