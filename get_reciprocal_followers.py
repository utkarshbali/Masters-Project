import pickle
import networkx as nx
import matplotlib.pyplot as plt

degrees = {}
degreeValues = {}
cc = {}
ccFreq = {}
triangles = {}
trianglesFreq = {}
clique = []
#kcomps = {}



def getReciprocalUsersGraph(UDG):
    nx.draw(UDG)
    plt.savefig("ReciprocalGraph_Di.png", format="PNG")
    plt.show()

def getGraph(DG):
    nx.draw(DG)
    plt.savefig("DiGraph.png", format="PNG")
    plt.show()

def updateDegreeFreq(value):
    if value in degreeValues:
        degreeValues[value] = degreeValues[value] + 1
    else: 
        degreeValues[value] = 1

def getDegreeHist(DG,nodes):
    for node in nodes:
        degrees[node] = nx.degree(DG,node)
    #degreeHist = nx.degree_histogram(DG)    
    for node in degrees:
        value = degrees[node]
        updateDegreeFreq(value)
    plt.hist(degreeValues.keys(),bins = 20)
    plt.xlabel('Degree', fontsize = 15)
    plt.ylabel('Frequency', fontsize = 15)
    plt.savefig("DegreeHistogram_Di.png", format="PNG")    
    plt.show()
def updateCCFreq(value):
    if value in ccFreq:
        ccFreq[value] = ccFreq[value] + 1
    else: 
        ccFreq[value] = 1
        
def getClusteringCoeff(UDG,nodes):
    for node in nodes:
        cc[node] = nx.clustering(UDG,node)
    #degreeHist = nx.degree_histogram(DG)    
    for node in cc:
        value = cc[node]
        updateCCFreq(value)
    plt.hist(ccFreq.keys(),bins = 20)
    plt.xlabel('Clustering Coefficient', fontsize = 15)
    plt.ylabel('Frequency', fontsize = 15)
    plt.savefig("ClusteringCoeffHistogram.png", format="PNG")    
    plt.show()
    
def updateTrianglesFreq(value):
    if value in trianglesFreq:
        trianglesFreq[value] = trianglesFreq[value] + 1
    else: 
        trianglesFreq[value] = 1
        
def getTriangles(UDG):
    triangles = nx.triangles(UDG)
    for node in triangles:
        value = triangles[node] 
        updateTrianglesFreq(value)
    plt.hist(trianglesFreq.keys(),bins = 20)
    plt.xlabel('Number Of Triangles', fontsize = 15)
    plt.ylabel('Frequency', fontsize = 15)
    plt.savefig("NumberOfTriangles.png", format="PNG")    
    plt.show()     
def getCliques(UDG):
    clique = nx.enumerate_all_cliques(UDG)
    clique = list(clique)
def getKCore(UDG):
    kCore = nx.k_core(UDG,k=10)
    nx.draw(kCore)
    plt.savefig("KCore.png", format="PNG")    
    plt.show()
    
def getKComps(UDG):
    kcomps = nx.k_components(UDG)
    
def main():
    #Read the picklefile containing graph
    DG = pickle.load(open("directed_followers_graph1.pkl","rb"))
    nodes = nx.nodes(DG)
    for node in nodes:
        degree = nx.degree(DG,node)
        if (degree == 0):
            DG.remove_node(node)
    nodes = nx.nodes(DG)
    UDG = DG.to_undirected(reciprocal = True)
    #getGraph(DG)
    #getReciprocalUsersGraph(UDG)
    #getDegreeHist(DG,nodes)
    #getClusteringCoeff(UDG,nodes)
    #getTriangles(UDG)
    #getCliques(UDG)
    #getKComps(UDG)
    getKCore(UDG)
if __name__ == "__main__":
    main()