import os
from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
import warnings
warnings.filterwarnings('ignore')
import re
import random
import json

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
    
    # Generate mock followers count (randomized for realism)
    followers = random.randint(10, 5000)

    # Generate mock friends (users with nearby IDs)
    friend_ids = [str(fid) for fid in range(num_users) if fid != user_id]
    random.shuffle(friend_ids)
    friends = friend_ids[:random.randint(1, num_users-1)]  # Each user gets 1-5 friends

    return {
        "user_id": str(user_id),
        "name": name.strip(),
        "followers": followers,
        "bio": bio.strip(),
        "posts": posts.strip(),
        "friends": friends
    }

def generate_data(num_users):
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
    data = {}
    i = 0
    user_id = 0
    while user_id < num_users: 
        raw_text = llm_chain.invoke({"user_id": i})
        while not valid_data(raw_text):
            i = i + 1
            raw_text = llm_chain.invoke({"user_id": i})
        user_profile = parse_profile(raw_text, user_id, num_users)
        user_id = user_id + 1
        data[user_id] = user_profile
            
    return data

if __name__ == "__main__":
    data = generate_data(100)

    # Create json file
    json_object = json.dumps( {"_default": data}, indent=4 )
    with open( "datastore/llmData_sns.json", "w" ) as f:
        f.write( json_object )
    