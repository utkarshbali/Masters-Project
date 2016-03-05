import pickle
import networkx as nx
import matplotlib.pyplot as plt

def getReciprocalUsersGraph(DG):
    DG.to_undirected(reciprocal = True)
    nx.draw(DG)
    plt.savefig("ReciprocalGraph.png", format="PNG")
    plt.show()

def getGraph(DG):
    nx.draw(DG)
    plt.savefig("Graph.png", format="PNG")
    plt.show()

def main():
    #Read the picklefile containing graph
    DG = pickle.load(open("directed_followers_graph.pkl","rb"))
    getGraph(DG)    
    getReciprocalUsersGraph(DG)    
    
if __name__ == "__main__":
    main()