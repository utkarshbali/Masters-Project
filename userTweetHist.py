#import nltk
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
        
def listUsers(f2):
    global users    
    for attribute, value in users.items():
        f2.write(attribute+'\n')        


def plotHistogram():
    global users, userCount, listNumberOfTweets
    listOfUsernames = list(users.keys())
    for i in range(0, len(listOfUsernames)):
        tweetCount = users[listOfUsernames[i]]
        updateNumberOfUsers(tweetCount)
    listNumberOfTweets = list(userCount.keys())
    listNumberOfTweets.sort()
    listNumberOfUsers = []
    for i in range(0, len(listNumberOfTweets)):
        listNumberOfUsers.append(userCount[listNumberOfTweets[i]])
    
    tweets_vs_Users = plt.figure()
    plt.hist(userCount.keys(), bins=50);
    plt.xlabel('Number of Tweets', fontsize = 15)
    plt.ylabel('Number of Users', fontsize = 15)
    tweets_vs_Users.savefig('#Tweets_vs_#Users.png')
    
    tweets_vs_Users1 = plt.figure()
    bins = range(0, 15)
    plt.xticks(bins, ["%s" %np.power(2,i) for i in bins])
    plt.hist(np.log2(userCount.values()), log=True, bins=bins)
    plt.xlabel('Number of Tweets', fontsize = 15)
    plt.ylabel('Number of Users', fontsize = 15)
    tweets_vs_Users1.savefig('log.png')

def main():
    f = file ("1year_filtered/1year_filtered.json")
    f.seek (0)
   #Read File
    while True:
        line = f.readline()
        if line == "":
            break
        j = json.loads(line)
        #tokens = nltk.word_tokenize(j["text"].encode('ascii', 'ignore') )
        username = j["user"]["screen_name"]
        updateTweetCount(username)
    f.close()  
    #f2 = open ("usersList.txt","w")
    #listUsers(f2)
  
    #call plotHistogram
    plotHistogram()
    
if __name__ == "__main__":
    main()# -*- coding: utf-8 -*-