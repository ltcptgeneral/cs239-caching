import requests
import random
import json
from tqdm import tqdm
import time
from utils import print_report

baseurl = "http://localhost:8000"

endpoints = {
    "/user/{user_id}": 0.8,  # 80% read operations
    "/update_user/?user_id={user_id}&name=Test&followers=100&bio=Updated&posts=Updated": 0.2  # 20% write operations
}

# Fetch all user IDs
user_ids = json.loads(requests.get(baseurl + "/users").content)["ids"]

random.seed(0)

def generate_random():
    """Randomly generate a read or write request, favoring cache hits."""
    endpoint = random.choices(list(endpoints.keys()), list(endpoints.values()))[0]
    if endpoint == "/user/{user_id}":
        # Favor frequently accessed user IDs to increase hit ratio
        if len(user_ids) > 0:
            # Sample from a subset of user IDs to simulate frequent access
            frequent_users = user_ids[:int(len(user_ids) * 0.2)]  # 20% frequent users
            random_user = str(random.choice(frequent_users)) if random.random() < 0.7 else str(random.choice(user_ids))
        else:
            random_user = str(random.choice(user_ids))
    else:
        random_user = str(random.choice(user_ids))
    return baseurl + endpoint.replace("{user_id}", random_user)

times = []
hits = []

# Warm-up phase
# for _ in tqdm(range(1000)):
#     url = generate_random()
#     requests.get(url)

# Main testing phase
start = time.time()
for i in tqdm(range(10000)):
    url = generate_random()
    response = requests.get(url)

    try:
        content = json.loads(response.content)
        
        if "time_ms" in content:  # Only process if "time_ms" exists
            times.append(content["time_ms"])
            hits.append(content["source"] == "cache")

    except json.JSONDecodeError:
        print(f"Error decoding JSON: {response.content}")
        exit(1)
    except KeyError:
        print(f"Unexpected response format: {content}")
        exit(1)

end = time.time()

print_report(hits, times, end - start)