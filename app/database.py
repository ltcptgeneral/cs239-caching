
from tinydb import TinyDB, Query
from config import DB_FILE

DB_LOCATION = "database/datastore/" + DB_FILE

# Initialize TinyDB as a NoSQL key-value store
db = TinyDB(DB_LOCATION)
User = Query()

def get_user_ids():
    return [x["user_id"] for x in db.all()]

def get_user_profile(user_id):
    """Fetch user profile from TinyDB"""
    result = db.search(User.user_id == user_id)
    return result[0] if result else None

def update_user_profile(user_id, name, followers, bio, posts, friends):
    """Update user profile in TinyDB"""
    db.upsert({"user_id": user_id, "name": name, "followers": followers, "bio": bio, "posts": posts, "friends": friends}, User.user_id == user_id)

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
