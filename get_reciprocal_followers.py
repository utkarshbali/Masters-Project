import pickle
import networkx as nx
import matplotlib.pyplot as plt

degrees = {}
cc = {}
triangles = {}
clique = []
#kcomps = {}

def getReciprocalUsersGraph(UDG):
    nx.draw(UDG,node_size = 100)
    plt.title(r'$\mathrm{Reciprocal\ Graph}\ $',fontsize = 15)
    plt.savefig("ReciprocalGraph_Di.png", format="PNG")
    plt.show()

def getGraph(DG):
    nx.draw(DG,node_size = 100)
    plt.title(r'$\mathrm{Graph}\ $',fontsize = 15)
    plt.savefig("DiGraph.png", format="PNG")
    plt.show()

def getDegreeHist(DG,nodes):
    for node in nodes:
        degrees[node] = nx.degree(DG,node)
    plt.hist(degrees.values(),log = True,bins = 20,facecolor='green', alpha=0.75)
    plt.xlabel('Degree', fontsize = 15)
    plt.ylabel('Frequency', fontsize = 15)
    plt.title(r'$\mathrm{Degree\ Histogram}\ $',fontsize = 15)
    plt.savefig("DegreeHistogram.png", format="PNG")
    plt.grid(True)
    plt.axis([-200,1000,0.1,10000])
    plt.show()
        
def getClusteringCoeff(UDG,nodes):
    global cc
    for node in nodes:
        cc[node] = nx.clustering(UDG,node)
        cc[node] = round(cc[node],2)
    plt.hist(cc.values(),bins = 10,log = True,facecolor='green', alpha=0.75)
    plt.xlabel('Clustering Coefficient', fontsize = 15)
    plt.ylabel('Frequency', fontsize = 15)
    plt.title(r'$\mathrm{Clustering\ Coefficient\ Histogram}\ $',fontsize = 15)        
    plt.savefig("ClusteringCoeffHistogram.png", format="PNG")
    plt.grid(True)
    plt.axis([-0.1,1.1,0.1,10000])
    plt.show()
        
def getTriangles(UDG):
    global triangles
    triangles = nx.triangles(UDG)
    plt.hist(triangles.values(),bins = 50,log = True,facecolor='green', alpha=0.75)
    plt.xlabel('Number Of Triangles', fontsize = 15)
    plt.ylabel('Frequency', fontsize = 15)
    plt.title(r'$\mathrm{Triangles\ Histogram}\ $',fontsize = 15)    
    plt.savefig("trianglesHistogram.png", format="PNG")    
    plt.grid(True)
    plt.axis([-200,4500,0.1,10000])
    plt.show()

def getCliques(UDG):
    clique = nx.enumerate_all_cliques(UDG)
    clique = list(clique)
    
def getKCore(UDG):
    kCore = nx.k_core(UDG,k=10)
    nx.draw(kCore,node_size = 100)
    plt.title(r'$\mathrm{K-Core}\ $',fontsize = 15)
    plt.savefig("KCore.png", format="PNG")    
    plt.show()
    
def getKComps(UDG):
    kcomps = nx.k_components(UDG)
    return kcomps
    
def main():
    #Read the picklefile containing graph
    DG = pickle.load(open("directed_followers_graph.pkl","rb"))
    nodes = nx.nodes(DG)
    for node in nodes:
        if (nx.degree(DG,node) == 0):
            DG.remove_node(node)
    nodes = nx.nodes(DG)
    UDG = DG.to_undirected(reciprocal = True)
    getGraph(DG)
    getReciprocalUsersGraph(UDG)
    getDegreeHist(DG,nodes)
    getClusteringCoeff(UDG,nodes)
    getTriangles(UDG)
    #getCliques(UDG)
    #getKComps(UDG)
    getKCore(UDG)
if __name__ == "__main__":
    main()