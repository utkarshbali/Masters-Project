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
    #f = file (sys.argv[1])
    f = file ("13-2015_social_graph.json")
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
                for follower in followers:
                    DG.add_edge(follower,userId)
                    #print "added edge from " + str(follower)
                for friend in friends:
                    DG.add_edge(userId,friend)
                    #print "added edge to " + str(friend)                       
        except Exception as e:
            print e
    f.close()
    f = file ("directed_followers_graph.pkl", "wb")
    pickle.dump(DG, f)
    
if __name__ == "__main__":
    main()