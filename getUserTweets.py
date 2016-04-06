import json
import networkx as nx
import pickle

userTweets = {}
tweets = []

def main():
    global userTweets
    # Get json file to read from
    f = file ("1year_filtered/1year_filtered.json")
    DG = pickle.load(open("directed_followers_graph1.pkl","rb"))
    nodes = nx.nodes(DG)
    while True:
        try:
            line = f.readline()
            if line == "":
                break
            j = json.loads(line)
            timeStamp = j["created_at"]
            userId = j["user"]["id_str"]
            tweet = j["text"]
            if userId in nodes:
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
    #pickle.dump(userTweets,open("userTweets.pkl","wb"))
    pickle.dump(userTweets,open("/usr/space1/uvb6476/userTweets.pkl","wb"))
if __name__ == "__main__":
    main()