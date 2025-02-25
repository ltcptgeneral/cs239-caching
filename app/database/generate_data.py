import os
from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
import warnings
warnings.filterwarnings('ignore')
import re
import random
import json
from tinydb import TinyDB
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware
import math

HUGGINGFACEHUB_API_TOKEN = None
os.environ["HUGGINGFACEHUB_API_TOKEN"] = HUGGINGFACEHUB_API_TOKEN

def valid_data(text):
    match = re.search(r"([A-Za-z ]+)\|([A-Za-z &\-!]+)\|([A-Za-z .',!?&\-]+)", text)
    if not match:
        return False
    else:
        return True

def parse_profile(text, user_id, num_users):
    match = re.search(r"([A-Za-z ]+)\|([A-Za-z &\-!]+)\|([A-Za-z .',!?&\-]+)", text)
    name, bio, posts = match.groups()
    
    followers = random.randint(10, 5000)

    friend_ids = [str(fid) for fid in range(user_id) if fid != user_id]
    random.shuffle(friend_ids)
    friends = friend_ids[:random.randint(1, min(100, math.ceil(num_users/3)))] 

    return {
        "user_id": str(user_id),
        "name": name.strip(),
        "followers": followers,
        "bio": bio.strip(),
        "posts": posts.strip(),
        "friends": friends
    }

def generate_data(base_id, num_users):
    system_message = """You are a data generator creating user profiles for a social media app. 
    Always provide user profiles in this format: Name | Interest | Recent Activity.
    Do not include numbers, IDs, or assistant labels. Only return a properly formatted response.

    Example: Alice Wonderland | Exploring the world one frame at a time! | Just captured a stunning sunset."""
    prompt = ChatPromptTemplate ([
        ("system", system_message),
        ("user", "Generate a user profile for user {user_id}")
    ])

    llm = HuggingFaceEndpoint(
        task='text-generation',
        model="deepseek-ai/DeepSeek-R1",
        max_new_tokens=150,
        do_sample=True,
        top_k=60,
        temperature=1.0,
        top_p=0.9,
        huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN,
    )
    llm_chain = prompt | llm
    data = []
    i = base_id
    user_id = 0
    while user_id < num_users: 
        raw_text = llm_chain.invoke({"user_id": i})
        while not valid_data(raw_text):
            i = i + 1
            raw_text = llm_chain.invoke({"user_id": i})
        user_profile = parse_profile(raw_text, base_id + user_id, num_users)
        user_id = user_id + 1
        i = i + 1
        data.append(user_profile)
            
    return data

if __name__ == "__main__":
    base_id = input("Enter base id (check db to find the next consecutive user_id): ")
    num_users = input("Enter number of users to generate: ")
    data = generate_data(int(base_id), int(num_users))
    
    # Create json file
    file_path = "datastore/llmData_sns.json"
    global db
    db = TinyDB(file_path, storage=CachingMiddleware(JSONStorage), indent=4)
    db.insert_multiple(data)
    db.close()
    