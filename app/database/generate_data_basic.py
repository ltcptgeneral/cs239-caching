import random, string
from tinydb import TinyDB
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware

def randomstring(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))

def generate_data(base_id, num_users):
    data = []
    for i in range(num_users):
        data.append({
        "user_id": str(base_id + i),
        "name": randomstring(10),
        "followers": random.randint(1, 10000),
        "bio": randomstring(250),
        "posts": randomstring(100),
        "friends": random.choices(range(base_id + i - 1), k=random.randint(1, 50))
    })

    return data

base_id = input("Enter base id (check db to find the next consecutive user_id): ")
num_users = input("Enter number of users to generate: ")
data = generate_data(int(base_id), int(num_users))

# Create json file
file_path = "datastore/llmData_sns.json"
global db
db = TinyDB(file_path, storage=CachingMiddleware(JSONStorage), indent=4)
db.insert_multiple(data)
db.close()