import requests
import random
import json
import time
from tqdm import tqdm
from utils import print_report

baseurl = "http://localhost:8000"

# Fetch all user IDs and friends list
user_ids = json.loads(requests.get(baseurl + "/users").content)["ids"]
user_friends = json.loads(requests.get(baseurl + "/users_and_friends").content)

random.seed(0)

# Workload Configurations
workloads = {
    "random_read": {"read": 1.0, "write": 0.0},
    "read_heavy": {"read": 0.8, "write": 0.2},
    "write_heavy": {"read": 0.2, "write": 0.8},
    "frequent_users": {"read": 1.0, "write": 0.0, "frequent_percent": 0.7},
    "frequent_after_write": {"read": 0.7, "write": 0.3},
    "friend_based": {"read": 1.0, "write": 0.0, "friend_access": 0.7},
}

# Frequent users for workload testing (top 10 users)
frequent_users = user_ids[:10]

def generate_request(workload, last_updated=None):
    """Generate read or write requests based on workload type"""
    if random.random() < workload["read"]:
        user_id = select_user(workload, last_updated)
        return baseurl + f"/user/{user_id}", None, "GET"

    # Write operation (updates user profile)
    user_id = select_user(workload, last_updated)
    write_obj = { "user_id":user_id,"name": "UpdatedUser", "followers":"500","bio":"Updated","posts":"UpdatedPost"}
    url = baseurl + f"/update_user/"
    return url, write_obj, "POST"

def select_user(workload, last_updated):
    """Selects a user based on workload type"""
    if "frequent_percent" in workload and random.random() < workload["frequent_percent"]:
        return random.choice(frequent_users)

    if "friend_access" in workload and random.random() < workload["friend_access"]:
        return random.choice(user_friends.get(str(last_updated), user_ids))

    return random.choice(user_ids)

def run_workload(name, workload):
    """Run a workload and log performance metrics"""
    times = []
    hits = []
    start = time.time()
    last_updated = None

    for _ in tqdm(range(10000), desc=f"Running {name}"):
        url, data, method = generate_request(workload, last_updated)
        
        if( method == "GET" ):
            response = requests.request(method, url)
        else:
            response = requests.post(url, json = data)

        try:
            content = json.loads(response.content)
            if "time_ms" in content:
                times.append(content["time_ms"])
                hits.append(content["source"] == "cache")
                if method == "POST":
                    last_updated = content.get("user_id", last_updated)
        except (json.JSONDecodeError, KeyError):
            print(f"Error processing response: {response.content}")

    end = time.time()
    print(f"\n--- {name} Results ---")
    print_report(hits, times, end - start)

# Run all workloads
for workload_name, workload_config in workloads.items():
    run_workload(workload_name, workload_config)
