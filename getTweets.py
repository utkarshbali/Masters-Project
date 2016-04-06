import json
import networkx as nx
import pickle

users = {}
userTweets = {}
tweets = []

def getUsers():
    global users
    users = pickle.load(open('syracuseUsers.pkl','rb'))
    
def main():
    global userTweets
    getUsers()
    # Get json file to read from
    f = file ("syracuse-03-2016.json")
    while True:
        try:
            line = f.readline()
            if line == "":
                break
            j = json.loads(line)
            timeStamp = j["created_at"]
            userId = j["user"]["id_str"]
            tweet = j["text"]
            if userId in users:
                count = 0
                tweets = userTweets.get(userId,{})
                if (tweet in tweets):
                    count = tweets[tweet][0] + 1
                    timeStamp = tweets[tweet][1]
                tweets[tweet] = [count,timeStamp]
                userTweets[userId] = tweets
        except Exception as e:
            print e
    f.close()
    pickle.dump(userTweets,open("syracuseUserTweets.pkl","wb"))
if __name__ == "__main__":
    main()