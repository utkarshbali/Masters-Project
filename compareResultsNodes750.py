import random
import pickle
import networkx as nx
import numpy as np
import xlsxwriter

wordGraph = {}
name = ''

def getWordGraph():
    global wordGraph
    wordGraph = pickle.load(open("wordGraph_750.pkl","rb"))

def compareNumberOfEdges(masterGraph,wordGraph,worksheet,row):
    numberOfEdgesMasterGraph = nx.number_of_edges(masterGraph)
    numberOfEdgesWordGraph = nx.number_of_edges(wordGraph)
#    worksheet.write(row,1,numberOfEdgesMasterGraph)
#    worksheet.write(row,2,numberOfEdgesWordGraph)
    result = False
    if(numberOfEdgesMasterGraph >= numberOfEdgesWordGraph):
        result = True
#    worksheet.write(row,3,result)

    if result == True:
        return 1
    else:
        return -1

def compareAvgDegree(masterGraph,wordGraph,worksheet,row):
    masterDegrees = nx.degree(masterGraph)
    wordDegrees = nx.degree(wordGraph)
    masterDegreeList = list(masterDegrees.values())
    averageMasterDegree = np.mean(masterDegreeList)
    wordDegreeList = list(wordDegrees.values())
    averageWordDegree = np.mean(wordDegreeList)
#    worksheet.write(row,1,averageMasterDegree)
#    worksheet.write(row,2,averageWordDegree)
    result = False
    if(averageMasterDegree >= averageWordDegree):
        result = True
#    worksheet.write(row,3,result)
    
    if result == True:
        return 1
    else:
        return -1
    
def compareAvgClusteringCoeff(masterGraph,wordGraph,worksheet,row):
    avgClusteringMaster = nx.average_clustering(masterGraph)
    avgClusteringWord = nx.average_clustering(wordGraph)
#    worksheet.write(row,1,avgClusteringMaster)
#    worksheet.write(row,2,avgClusteringWord)

    result = False
    if(avgClusteringMaster >= avgClusteringWord):
        result = True
#    worksheet.write(row,3,result)
    
    if result == True:
        return 1
    else:
        return -1

def compareAvgNumberOfTriangles(masterGraph,wordGraph,worksheet,row):
    masterTriangles = nx.triangles(masterGraph)
    wordTriangles = nx.triangles(wordGraph)
    numberOfTrianglesMaster = list(masterTriangles.values())
    numberOfTrianglesWord = list(wordTriangles.values())
    averageNumberOfTrianglesMaster = (np.mean(numberOfTrianglesMaster)/3)
    averageNumberOfTrianglesWord = (np.mean(numberOfTrianglesWord)/3)
#    worksheet.write(row,1,averageNumberOfTrianglesMaster)
#    worksheet.write(row,2,averageNumberOfTrianglesWord)

    result = False
    if(averageNumberOfTrianglesMaster >= averageNumberOfTrianglesWord):
        result = True
#    worksheet.write(row,3,result)
    
    if result == True:
        return 1
    else:
        return -1

def compareLargestCC(masterGraph,wordGraph,worksheet,row):
    largestCCMaster = max(nx.connected_components(masterGraph))
    largestCCWord = max(nx.connected_components(wordGraph))
#    worksheet.write(row,1,len(largestCCMaster))
#    worksheet.write(row,2,len(largestCCWord))

    result = False
    if(len(largestCCMaster) >= len(largestCCWord)):
        result = True
#    worksheet.write(row,3,result)
    
    if result == True:
        return 1
    else:
        return -1
    
def main():
    global name
    DG = pickle.load(open('directed_followers_graph.pkl','rb'))
    getWordGraph()
    wordRank = 1146147/750
    fName = "Nodes"+str(wordRank) + ".xlsx"
    filename = file(fName,"wb")  
    workbook = xlsxwriter.Workbook(filename)
    bold = workbook.add_format({'bold': True})
    worksheet = workbook.add_worksheet("Results")
    worksheet.set_column(0, 4, 30)
    #count = wordGraph beats mastergraph
    worksheet.write(0,0,"word",bold)
    worksheet.write(0,1,"Word Graph Edges",bold)    
    worksheet.write(0,2,"Average Master Graph Edges",bold)
    worksheet.write(0,3,"Word Graph Nodes",bold)
    worksheet.write(0,4,"Average Master Graph Nodes",bold)
    worksheet.write(0,5,"Average Degree Count",bold)
    worksheet.write(0,6,"Average Clustering Coefficient Count",bold)
    worksheet.write(0,7,"Average number of triangles Count",bold)
    worksheet.write(0,8,"Largest Connected Component Count",bold)
    row = 0
    for value in wordGraph:        
        if value == ". .":
            name = "dotDot"
        elif value == ".......":
            name = 'dotDotDotDot'
        elif value == "24/7":
            name = '24X7'
        elif value == "@teamginger_":
            name = '@teamginger'
        elif value == ":p":
            name = 'tongueSmiley'
        elif value == ":D":
            name = 'laughterSmiley'
        elif value == "1:00":
            name = 'oneOClock'
        else:
            name = value
        row = row + 1
        countNodes = 0
        countDegree = 0
        countAvgClusteringCoeff = 0
        countAvgTriangles = 0
        countLargestCC = 0
        numEdgesMasterGraph = 0
        graph =  wordGraph[value]
        undirectedGraph = graph.to_undirected()
        nodes = nx.nodes(DG)
        numberOfNodes = nx.number_of_nodes(graph)
        if numberOfNodes > 0:
            for i in range(0,1000):  
                masterGraphNodes = random.sample(nodes,numberOfNodes)
                masterGraph = DG.subgraph(masterGraphNodes)
                numEdges = nx.number_of_edges(masterGraph)
                numEdgesMasterGraph = numEdgesMasterGraph + numEdges
                undirectedMasterGraph = masterGraph.to_undirected()
                nodesResult = compareNumberOfEdges(undirectedMasterGraph,graph,worksheet,row + 2)
                if nodesResult == -1:
                    countNodes = countNodes + 1
                degreeResult = compareAvgDegree(undirectedMasterGraph,graph,worksheet,row + 3)
                if degreeResult == -1:
                    countDegree = countDegree + 1
                clusteringCoeffResult = compareAvgClusteringCoeff(undirectedMasterGraph,undirectedGraph,worksheet,row + 4)
                if clusteringCoeffResult == -1:
                    countAvgClusteringCoeff = countAvgClusteringCoeff + 1
                numberOfTrianglesResult = compareAvgNumberOfTriangles(undirectedMasterGraph,undirectedGraph,worksheet,row + 5)
                if numberOfTrianglesResult == -1:
                    countAvgTriangles = countAvgTriangles + 1
                LargestCCResult = compareLargestCC(undirectedMasterGraph,undirectedGraph,worksheet,row + 6)
                if LargestCCResult == -1:
                    countLargestCC = countLargestCC + 1
                
        worksheet.write(row,0,value,bold)
        edges = nx.number_of_edges(graph)
        worksheet.write(row,1,edges,bold)
        avgEdges = float(numEdgesMasterGraph)/1000
        worksheet.write(row,2,avgEdges,bold)
        worksheet.write(row,3,numberOfNodes,bold)
        worksheet.write(row,4,numberOfNodes,bold)
        worksheet.write(row,5,countDegree,bold)
        worksheet.write(row,6,countAvgClusteringCoeff,bold)
        worksheet.write(row,7,countAvgTriangles,bold)
        worksheet.write(row,8,countLargestCC,bold)
    workbook.close()

if __name__ == "__main__":
    main()# -*- coding: utf-8 -*-