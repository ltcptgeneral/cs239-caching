# Quick script to create basic dummy data for the caching system
# Current theme/usage is in a social media microservice setting such as Twitter
# Current database schema:
### user_id (primary key), str
### username, string
### num_followers, int
### posts, str (for now, can be list later on)
### friends, list[user_id]

import json
import random

# Parameters to change the distribution/random ranges
TOTAL_USERS = 20
MIN_FOLLOWERS, MAX_FOLLOWERS = 0, 5
MIN_POSTS, MAX_POSTS = 5, 10
MIN_FRIENDS, MAX_FRIENDS = 1, 5

# Create the user data
# TODO if we want to vary the user data more, we can inflate the posts into a list of strings and make the strings very long :3"
data = {}
for user_id in range( TOTAL_USERS ):
    user = {}
    user["user_id"] = str( user_id )
    user["username"] = "user" + str( user_id )
    user["num_followers"] = random.randint( MIN_FOLLOWERS, MAX_FOLLOWERS )
    
    # Just make a single post for now, can consider mutliple posts later
    user["posts"] = f"This is user {user_id}'s post!"

    # posts = []
    # for post_num in range( random.randint( MIN_FOLLOWERS, MAX_FOLLOWERS ) ):
    #     posts.append( f"This is user {user_id}'s post {str( post_num + 1 )}!" )
    # user["posts"] = posts
    
    friends = []
    user["friends"] = random.sample( [u_id for u_id in range( TOTAL_USERS ) if u_id != user_id], random.randint( MIN_FOLLOWERS, MAX_FOLLOWERS ) )

    data[user_id] = user

# Load the data into a json object and write it into the datastore folder
json_object = json.dumps( {"_default": data}, indent=4 )
with open( "datastore/basicDummy_sns.json", "w" ) as f:
    f.write( json_object )
