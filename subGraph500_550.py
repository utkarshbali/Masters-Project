import pickle
import networkx as nx
import datetime

top50 = []
words = {}
userTerms = {}
wordGraph = {}

def getUserTerms():
    global userTerms
    userTerms = pickle.load(open("userTerms.pkl","rb"))
    
def getWords():
    global words
    words = pickle.load(open("topWords.pkl","rb"))

def getTop50Words():
    global top50
    getWords()
    for i in range(500,len(words)):
        if len(top50) == 50:
            break
        word = words[i][0].encode('ascii','ignore')
        if (word != ''):
            top50.append(word)
   
def main():
    global wordGraph

    DG = pickle.load(open("directed_followers_graph.pkl","rb"))
    getUserTerms()
    getTop50Words()
    
    for word in top50:
        subGraph = nx.DiGraph()
        for user in userTerms:
            info = userTerms[user]
            if word in info:
                userTimeStamp = userTerms[user][word][1]
                convUserTimeStamp = datetime.datetime.strptime(userTimeStamp,'%a, %d %b %Y %H:%M:%S +0000')
                edges = DG.out_edges(user)               
                for followers in edges:
                    follower = followers[1]
                    if follower in userTerms:
                        if word in userTerms[follower]:
                            followerTimeStamp = userTerms[follower][word][1]
                            convFollowerTimeStamp = datetime.datetime.strptime(followerTimeStamp,'%a, %d %b %Y %H:%M:%S +0000')
                            if(convUserTimeStamp < convFollowerTimeStamp):
                                if user not in subGraph:
                                    #print "adding node "+ user + " to graph"
                                    subGraph.add_node(user)
                                if follower not in subGraph:
                                    #print "adding node "+ follower + " to graph"
                                    subGraph.add_node(follower)
                                #print "adding node edge from " + user + " to " + follower+ " in graph"
                                subGraph.add_edge(user,follower)
        #print "Graph for "+word+" Complete"
        nx.draw(subGraph)
        wordGraph[word] = subGraph
    #print wordGraph

    pickle.dump(wordGraph,open('wordGraph_500_550.pkl','wb'))

if __name__ == "__main__":
    main()# -*- coding: utf-8 -*-
