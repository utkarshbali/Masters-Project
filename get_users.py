# get_users.py
# Author: Utkarsh Bali
#
# Goes through 1year_filtered.json and creates a dictionary that maps 
# userids to number of tweets. 
# Writes this info to a pkl file call users.pkl
#
# usage:
# python get_users.py JSON_FILE
# E.g.
# python get_users.py oneyear.filtered.json

import json
import pickle
import sys

users = {}

# Update count of tweets for user if user already exists in 
# users dictionary else set the count to 1
def updateTweetCount(userId):
    global users
    if(userId in users):
           currentCount = users[userId]
           users[userId] = currentCount + 1
    else:
        users[userId] = 1

def main():
    # Get json file to read from    
    #f = file ("1year_filtered/1year_filtered.json")
    f = file (sys.argv[1])
    f.seek (0)
   #Read File
    while True:
        line = f.readline()
        if line == "":
            break
        j = json.loads(line)
        # Get user id
        userId = j["user"]["id_str"]
        # Map the user ids to number of tweets
        updateTweetCount(userId)
    f.close()
    
    # Write users to a pickle file
    pickle.dump(users,open("users.pkl","wb"))

if __name__ == "__main__":
    main()# -*- coding: utf-8 -*-