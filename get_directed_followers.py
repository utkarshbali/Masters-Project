import pickle
import sys
import json
import networkx as nx
import matplotlib.pyplot as plt

users = {}
relevantUsers = []
followers = {}
friends = {}
# Read the picklefile containing users and number of tweets
def getUsers():
    global users
    users = pickle.load(open("users.pkl","rb"))
    
def getRelevantUsers():
    global relevantUsers,users
    getUsers() 
    relevantUsers = []
    for user in users:
        if users[user] >= 50:
            relevantUsers.append(user)
    return relevantUsers

def main():
    global users,followers,friends,relevantUsers
    # Get json file to read from
    f = file (sys.argv[1])
    #f = file ("13-2015_social_graph.json")
    relevantUsers = getRelevantUsers()
    DG = nx.DiGraph()
    
    while True: 
        try:
            line = f.readline()
            if line == "":
                break
            j = json.loads(line)
            userId = j["user_id"]
            if userId in relevantUsers:
                DG.add_node(userId)
                #print "Added Node" + userId                
                followers[userId] = j["follower_ids"]
                friends[userId] = j["friend_ids"]
        except Exception as e:
            print e

    nodes = nx.nodes(DG)
    for user in followers:
        #followersList = followers[user] 
        #for follower in followersList:
        for follower in followers[user]:
            follower = str(follower)
            if follower in nodes and user in nodes and user!=follower:
                DG.add_edge(follower,user)
    for user in friends:
        #friendsList = friends[user] 
        #for follower in friendsList:
        for friend in followers[user]:
            friend = str(friend)
            if friend in nodes and user in nodes and user!=friend:
                DG.add_edge(user,friend)
                
    f.close()
    f = file ("directed_followers_graph.pkl", "wb")
    pickle.dump(DG, f)
    
if __name__ == "__main__":
    main()