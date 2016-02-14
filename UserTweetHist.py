import nltk
#import sys
#import re
import json
#import networkx as nx
#import pickle
import matplotlib.pyplot as plt
import numpy as np

# Create dictionary to store number of tweets by a particular user
users = {}

# Update count of tweets for user if user already exists in users 
# dictionary else set the count to 1
def updateTweetCount(username):
    global users
    if(username in users):
           currentCount = users[username]
           users[username] = currentCount + 1
    else:
        users[username] = 1
        
# Create dictionary to store count of users having 
# a particular number of tweets
userCount = {}

# Update count of users if user already exists in userCount dictionary
# else set the count to 1
def updateNumberOfUsers(tweetCount):
    global userCount
    if(tweetCount in userCount):
           currentCount = userCount[tweetCount]
           userCount[tweetCount] = currentCount + 1
    else:
        userCount[tweetCount] = 1

def plotHistogram():
    global users, userCount
    listOfUsernames = list(users.keys())
    for i in range(0, len(listOfUsernames)):
        tweetCount = users[listOfUsernames[i]]
        updateNumberOfUsers(tweetCount)
    listNumberOfTweets = list(userCount.keys())
    listNumberOfUsers = []
    for i in range(0, len(listNumberOfTweets)):
        listNumberOfUsers.append(listNumberOfTweets[i])
    
    tweets_vs_Users = plt.figure()
    plt.bar(np.arange(len(listNumberOfUsers)), listNumberOfUsers)
    plt.xticks(np.arange(len(listNumberOfUsers)) + .25/2, listNumberOfTweets)
    plt.xlabel('Number of Tweets', fontsize = 15)
    plt.ylabel('Number of Users', fontsize = 15)
    tweets_vs_Users.savefig('#Tweets_v/s_#Users.pdf')
    

def main():

    f = file (sys.argv[1])
  
    f.seek (0)
    #Read File   
    while True:
        line = f.readline()
        if line == "":
            break
        j = json.loads(line)
        tokens = nltk.word_tokenize(j["text"].encode('ascii', 'ignore') )
        for i, x in enumerate(tokens):
            try:
                if x == "@":
                    username = j["user"]["screen_name"]
                    updateTweetCount(username)
            except IndexError:
                pass
        
    f.close()

    #call plotHistogram
    plotHistogram()
    
if __name__ == "__main__":
    main()# -*- coding: utf-8 -*-

