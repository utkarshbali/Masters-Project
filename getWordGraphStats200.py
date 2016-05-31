import pickle
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import xlsxwriter
import os
import math

wordGraph = {}
name = ''
zeroNodes = []
count = 0

def getWordGraph():
    global wordGraph
    wordGraph = pickle.load(open("wordGraph_200.pkl","rb"))

def getNumberOfNodes(graph,worksheet):
    numberOfNodes = nx.number_of_nodes(graph)
    worksheet.write(1,0,numberOfNodes)
    print "numberOfNodes : " + str(numberOfNodes)

def getAvgDegree(graph,worksheet):
    degrees = nx.degree(graph)
    degreeList = list(degrees.values())
    averageDegree = np.mean(degreeList)
    worksheet.write(1,1,averageDegree)
    print "averageDegree : " + str(averageDegree)
    
def getDegreeHist(graph,nodes,worksheet):
    global name
    degrees = {}
    for node in nodes:
        degrees[node] = nx.degree(graph,node)
    directory = "wordGraphs/200/"+name
    directory = os.path.normpath(directory)
    if not os.path.exists(directory):
        os.makedirs(directory)    
    path = directory +"/DegreeHistogram.png"    
    fileName = os.path.normpath(path)
    plt.hist(degrees.values(),log = True,bins = 10,facecolor='green', alpha=0.75)
    plt.xlabel('Degree', fontsize = 15)
    plt.ylabel('Frequency', fontsize = 15)
    plt.title(r'$\mathrm{Degree\ Histogram\ for\ }'+name+'\ $',fontsize = 15)
    plt.grid(True)
    xMax = int(math.ceil(max(degrees.values()) / 50.0)) * 50
    plt.axis([0,xMax,0.1,1000])
    plt.savefig(fileName, format="PNG")
    plt.show()
    worksheet.insert_image(4,1,fileName, {'x_scale': 0.5, 'y_scale': 0.5})

def getAvgClusteringCoeff(graph,worksheet):
    avgClustering = nx.average_clustering(graph)
    print "avgClustering : " + str(avgClustering)
    worksheet.write(1,2,avgClustering)
    
def getClusteringCoeffHist(graph,nodes,worksheet):
    global name    
    cc = {}
    for node in nodes:
        cc[node] = nx.clustering(graph,node)
        cc[node] = round(cc[node],2)
    directory = "wordGraphs/200/"+name
    directory = os.path.normpath(directory)
    if not os.path.exists(directory):
        os.makedirs(directory)    
    path = directory + "/ClusteringCoeffHistogram.png"
    fileName = os.path.normpath(path)
    plt.hist(cc.values(),bins = 10,log = True,facecolor='green', alpha=0.75)
    plt.xlabel('Clustering Coefficient', fontsize = 15)
    plt.ylabel('Frequency', fontsize = 15)
    plt.title(r'$\mathrm{Clustering\ Coefficient\ Histogram\ for\ }' + name + ' \ $',fontsize = 15)        
    plt.savefig(fileName, format="PNG") 
    plt.grid(True)
    plt.axis([-0.1,1.1,0.1,1000])
    plt.show()
    worksheet.insert_image(4,2,fileName, {'x_scale': 0.5, 'y_scale': 0.5})

def getAvgNumberOfTriangles(graph,worksheet):
    triangles = nx.triangles(graph)
    numberOfTriangles = list(triangles.values())
    averageNumberOfTriangles = (np.mean(numberOfTriangles)/3)
    worksheet.write(1,3,averageNumberOfTriangles)
    print "numberOfTriangles : " + str(averageNumberOfTriangles)

def getTrianglesHist(graph,worksheet):
    global name
    triangles = {}
    triangles = nx.triangles(graph)
    directory = "wordGraphs/200/"+name
    directory = os.path.normpath(directory)
    if not os.path.exists(directory):
        os.makedirs(directory)    
    path = directory +"/trianglesHistogram.png"
    fileName = os.path.normpath(path)
    plt.hist(triangles.values(),bins = 10,log = True,facecolor='green', alpha=0.75)
    plt.xlabel('Number Of Triangles', fontsize = 15)
    plt.ylabel('Frequency', fontsize = 15)
    plt.title(r'$\mathrm{Triangles\ Histogram\ for\ }' + name +'\ $',fontsize = 15)    
    plt.savefig(fileName, format="PNG")
    plt.grid(True)
    xMax = int(math.ceil(max(triangles.values()) / 50.0)) * 50
    plt.axis([0,xMax,0.1,1000])
    plt.show()    
    worksheet.insert_image(4,3,fileName, {'x_scale': 0.5, 'y_scale': 0.5})

def getLargestCC(graph,worksheet):
    largestCC = max(nx.connected_components(graph))
    print "largestCC : "+ str(len(largestCC))
    worksheet.write(1,4,len(largestCC))
    
def getKCore(graph,worksheet):
    global name
    kCore = nx.k_core(graph)
    print 'KCore : '
    directory = "wordGraphs/200/"+name
    directory = os.path.normpath(directory)
    if not os.path.exists(directory):
        os.makedirs(directory)    
    path = directory +"/KCore.png"
    fileName = os.path.normpath(path)
    nx.draw(kCore,node_size=100)
    plt.title(r'$\mathrm{K-Core\ for\ }' + name +'\ $',fontsize = 15)
    plt.savefig(fileName, format="PNG")
    plt.show()
    worksheet.insert_image(4,5,fileName, {'x_scale': 0.5, 'y_scale': 0.5})
    
def getGraph(graph,worksheet):
    global name
    print 'Graph : '
    nx.draw(graph,pos=nx.spring_layout(graph),node_size=100)
    directory = "wordGraphs/200/"+name
    directory = os.path.normpath(directory)
    if not os.path.exists(directory):
        os.makedirs(directory)    
    path = directory +"/Graph.png"
    fileName = os.path.normpath(path)
    plt.title(r'$\mathrm{Graph\ for\ }'+name+'\ $',fontsize = 15)
    plt.savefig(fileName, format="PNG")
    plt.show()
    worksheet.insert_image(4,6,fileName, {'x_scale': 0.5, 'y_scale': 0.5})
    
def main():
    global name,zeroNodes,count
    getWordGraph()
    filename = file("Word Graph_200.xlsx","wb")  
    workbook = xlsxwriter.Workbook(filename)
    bold = workbook.add_format({'bold': True})
    for value in wordGraph:
        count = count + 1
        if value == ". .":
            name = "dotDot"
        elif value == ".......":
            name = 'dotDotDotDot'
        elif value == "1:00":
            name = 'one o-clock'
        elif value == "@reginaape_":
            name = '@reginaape'
        elif value == "@cuntney_":
            name = '@cuntney'
        elif value == "8:":
            name = '8emoji'
        elif value == "]:":
            name = 'sadEmoji'
        else:
            name = value
        print name
        print count
        worksheet = workbook.add_worksheet(name)
        worksheet.set_column(0, 6, 50)
        worksheet.write(0,0,"Number of Nodes",bold)
        worksheet.write(0,1,"Average Degree",bold)
        worksheet.write(0,2,"Average Clustering Coefficient",bold)
        worksheet.write(0,3,"Average number of triangles",bold)
        worksheet.write(0,4,"Largest Connected Component",bold)
        worksheet.write(0,5,"KCore",bold)
        worksheet.write(0,6,"Graph",bold)
        graph =  wordGraph[value]
        undirectedGraph = graph.to_undirected()
        nodes = nx.nodes(graph)
        getNumberOfNodes(graph,worksheet)
        numberOfNodes = nx.number_of_nodes(graph)
        if numberOfNodes > 0:
            getAvgDegree(graph,worksheet)
            getDegreeHist(graph,nodes,worksheet)
            getAvgClusteringCoeff(undirectedGraph,worksheet)
            getClusteringCoeffHist(undirectedGraph,nodes,worksheet)
            getAvgNumberOfTriangles(undirectedGraph,worksheet)
            getTrianglesHist(undirectedGraph,worksheet)
            getLargestCC(undirectedGraph,worksheet)
            getKCore(undirectedGraph,worksheet)
            getGraph(graph,worksheet)
        else:
            zeroNodes.append(name)
    workbook.close()

if __name__ == "__main__":
    main()# -*- coding: utf-8 -*-