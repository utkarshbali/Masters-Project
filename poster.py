import networkx as nx
import pickle
import matplotlib.pyplot as plt

def getWordGraph():
    wordGraph = pickle.load(open("wordGraph_200.pkl","rb"))
    return wordGraph
    
def getKCore(undirectedGraph):
    pos = nx.spring_layout(undirectedGraph,k=0.15,iterations=20)
    nx.draw(undirectedGraph,pos,node_size=100,node_color = 'k')
    kCore = nx.k_core(undirectedGraph)
    kCore_edges = nx.edges(kCore)
    nx.draw_networkx_nodes(undirectedGraph,pos,nodelist=kCore,node_color='b',node_size = 100)    
    nx.draw_networkx_edges(undirectedGraph,pos,edgelist=kCore_edges,edge_color='b',width=3)
#    fig = plt.gcf()    
#    fig.set_size_inches((10, 10))
    plt.savefig('kcore.eps', format='eps', dpi=1000)
    plt.show()
    
def getLargestCC(undirectedGraph):
    pos = nx.spring_layout(undirectedGraph,k=0.15,iterations=20)
    nx.draw(undirectedGraph,pos,node_size=100,node_color = 'k')
    largestCC = max(nx.connected_components(undirectedGraph))
    cc = nx.Graph()
    cc.add_path(largestCC)
    cc_edges = nx.edges(cc)
    nx.draw_networkx_nodes(undirectedGraph,pos,nodelist=largestCC,node_color='g',node_size = 100)
    nx.draw_networkx_edges(undirectedGraph,pos,edgelist=cc_edges,edge_color='g',width=3)
#    fig = plt.gcf()    
#    fig.set_size_inches((10, 10))
    plt.savefig('cc.eps', format='eps', dpi=1000)
    plt.show()
    
def getGraph(undirectedGraph):
    graph = pickle.load(open('directed_followers_graph.pkl','rb'))
    nodes = nx.nodes(undirectedGraph)
    e = nx.edges(undirectedGraph)
    x = e
    for node in nodes:
        neighbours = nx.neighbors(graph,node)
        for n in range(0,(len(neighbours))):
            if(n <= 4):
                neighbour = neighbours[n]
                undirectedGraph.add_node(neighbour)
                undirectedGraph.add_edge(node,neighbour)
    
    pos = nx.spring_layout(undirectedGraph,k=0.15,iterations=20)
    
    nx.draw(undirectedGraph,pos,node_color = 'lightgray',node_size = 50,edgelist = nx.edges(undirectedGraph),edge_color = 'lightgray')
    nx.draw_networkx_nodes(undirectedGraph,pos,nodelist=nodes,node_color='r',node_size = 100)
    nx.draw_networkx_edges(undirectedGraph,pos,edgelist=x,edge_color='r',width=2)
    fig = plt.gcf()    
    fig.set_size_inches((10, 10))
    plt.savefig('graph.eps', format='eps', dpi=1000)
    plt.show()
    
def getTriangles(undirectedGraph):
    pos = nx.spring_layout(undirectedGraph,k=0.15,iterations=20)
    cycls_3 = [c for c in nx.cycle_basis(undirectedGraph) if len(c)==3]
    cycls_3=cycls_3[1]
    sub = nx.Graph()
    sub.add_cycle(cycls_3)
    sub_edges = nx.edges(sub)
    nx.draw(undirectedGraph,pos,node_size=100,node_color = 'k')    
    nx.draw_networkx_nodes(undirectedGraph,pos,nodelist=cycls_3,node_color='m',node_size = 100)
    nx.draw_networkx_edges(undirectedGraph,pos,edgelist=sub_edges,edge_color='m',width=3)
#    fig = plt.gcf()    
#    fig.set_size_inches((10, 10))    
    plt.savefig('triangles.eps', format='eps', dpi=1000)    
    plt.show

def getNeighbours(undirectedGraph):
    triangles = nx.triangles(undirectedGraph)
    node = '587152115'
#    print triangles[node]
    color=[]
    for n in nx.nodes(undirectedGraph):
        if n == node:        
            color.append('k')
        else:
            color.append('lightgray')
        
    ego = nx.ego_graph(undirectedGraph,node)    
    pos = nx.spring_layout(undirectedGraph,k=0.15,iterations=20)
    nx.draw(undirectedGraph,pos,node_size=100,node_color = color)    
    nx.draw_networkx_nodes(undirectedGraph,pos,nodelist=ego,node_color='blue',node_size = 100)
    nx.draw_networkx_edges(undirectedGraph,pos,edgelist=nx.edges(ego),edge_color='blue',width=2)
    nx.draw_networkx_nodes(undirectedGraph,pos,nodelist=[node],node_color='red',node_size = 100)
#    fig = plt.gcf()    
#    fig.set_size_inches((6, 6))    
    plt.savefig('cluster.eps', format='eps', dpi=1000)    
    plt.show
    
def main():
    global kCore
    wordGraph = getWordGraph()
    for value in wordGraph:
        if value == "#rochesterny":
            graph = wordGraph[value]
            undirectedGraph = graph.to_undirected()
#            getGraph(undirectedGraph)
#            getLargestCC(undirectedGraph)
#            getKCore(undirectedGraph)
#            getTriangles(undirectedGraph)
            getNeighbours(undirectedGraph)

    

if __name__ == "__main__":
        main()
