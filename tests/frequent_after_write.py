import requests
import random
import json
from tqdm import tqdm
import time
from collections import deque
from utils import print_report

baseurl = "http://localhost:8000"

endpoints = {
    "/user/{user_id}": 0.5,  # 50% read operations
    "/update_user/?user_id={user_id}&name=Test&followers=100&bio=Updated&posts=Updated": 0.5  # 50% write operations
}

# Fetch all user IDs
user_ids = json.loads(requests.get(baseurl + "/users").content)["ids"]

random.seed(0)

prev_updated_users = deque()
def generate_random():
    """Randomly generate a read or write request, favoring cache hits."""
    endpoint = random.choices(list(endpoints.keys()), list(endpoints.values()))[0]
    # Reads
    if endpoint == "/user/{user_id}":
        # Favor frequently accessed user IDs to increase hit ratio
        if( prev_updated_users ):
            random_user = str(random.choice(prev_updated_users)) if random.random() < 0.7 else str(random.choice(user_ids))
        else:
            random_user = str(random.choice(user_ids))
        return baseurl + endpoint.replace("{user_id}", random_user)
    # Writes
    else:
        random_user = str(random.choice(user_ids))
        prev_updated_users.append( random_user )
        if( len( prev_updated_users ) > 10 ):
            prev_updated_users.popleft()
        return random_user
    
times = []
hits = []

start = time.time()
for i in tqdm(range(10000)):
    url = generate_random()

    if( "user" not in url ):
        write_obj = { "user_id":url,"name": "Test", "followers":"100","bio":"updated","posts":"updated"}
        response = requests.post("http://localhost:8000/update_user/", json = write_obj)
    else:
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

print(f"\n--- Results ---")
print_report(hits, times, end - start)