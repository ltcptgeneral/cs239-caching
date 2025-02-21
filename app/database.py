
from tinydb import TinyDB, Query
from generate_data import generate_data

# Initialize TinyDB as a NoSQL key-value store
DB_FILE = "database.json"
db = TinyDB(DB_FILE)
User = Query()

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
    db = TinyDB(DB_FILE)  # Reload TinyDB if needed

    # Prepopulate database with some sample users if empty
    if len(db) == 0:
        data = generate_data(100)
        db.insert_multiple(data)
