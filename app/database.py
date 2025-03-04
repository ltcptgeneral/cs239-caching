from tinydb import TinyDB, Query
from config import DB_FILE
import shutil

import random

DB_LOCATION = "database/datastore/" + DB_FILE

# Initialize TinyDB as a NoSQL key-value store
# We don't want to change our main DB file, so we will make a temp DB file and use that as our DB file
shutil.copyfile( DB_LOCATION, "temp_DB.json" )

db = TinyDB("temp_DB.json")
User = Query()

def get_user_ids():
    return [x["user_id"] for x in db.all()]

def get_user_friend_ids():
    user_friends = {}
    for x in db.all():
        user_friends[x["user_id"]] = x["friends"]
    return user_friends

def get_friends(user_id, num_friends):
    friends = {}
    curr_user = db.search(User.user_id == user_id)
    random.seed(0)
    if not curr_user:
        return {}
    for f in random.sample(curr_user[0]["friends"], num_friends):
        friends[f] = db.search(User.user_id == user_id)[0]
    return friends

def get_user_profile(user_id):
    """Fetch user profile from TinyDB"""
    result = db.search(User.user_id == user_id)
    return result[0] if result else None

def update_user_profile( data ):
    """Update user profile in TinyDB"""
    user_id = str( data["user_id"] )

    # Basically make sure friends stay the same (for prefetching). Not great implementation, but it works
    curr_user = db.search(User.user_id == user_id)
    if( curr_user and data["friends"] == None ):
        data["friends"] = curr_user[0]["friends"]

    db.upsert( data, User.user_id == user_id )

def init_db():
    """Ensure TinyDB is initialized before FastAPI starts and prepopulate some data"""
    global db
    db = TinyDB(DB_LOCATION)  # Reload TinyDB if needed

    # Prepopulate database with some sample users if empty
    if len(db) == 0:
        db.insert_multiple([
            {"user_id": "1", "name": "Alice", "followers": 100, "bio": "Love coding!", "posts": "Hello, world!", "friends": ["2"]},
            {"user_id": "2", "name": "Bob", "followers": 200, "bio": "Tech enthusiast", "posts": "AI is amazing!","friends": ["3", "1"]},
            {"user_id": "3", "name": "Charlie", "followers": 50, "bio": "Blogger", "posts": "Check out my latest post!", "friends": ["1"]}
        ])
