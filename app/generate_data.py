import os
from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
import warnings
warnings.filterwarnings('ignore')
import re
import random

HUGGINGFACEHUB_API_TOKEN = None
os.environ["HUGGINGFACEHUB_API_TOKEN"] = HUGGINGFACEHUB_API_TOKEN

def parse_profile(text, user_id, num_users):
    match = re.search(r"([A-Za-z ]+)\|([A-Za-z &\-!]+)\|([A-Za-z .',!?&\-]+)", text)
    if not match:
        return None  # Skip invalid responses

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
    # prompt = PromptTemplate.from_template(template)
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
    for i in range(num_users): 
        raw_text = llm_chain.invoke({"user_id": i})
        user_profile = parse_profile(raw_text, i, num_users)
        if user_profile:
            data.append(user_profile)
            
    return data