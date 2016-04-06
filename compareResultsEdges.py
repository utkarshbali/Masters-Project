import random
import pickle
import networkx as nx
import numpy as np
import xlsxwriter

wordGraph = {}
name = ''

def getWordGraph():
    global wordGraph
    wordGraph = pickle.load(open("wordGraph_mid.pkl","rb"))

def compareNumberOfNodes(masterGraph,wordGraph,worksheet,row):
    numberOfNodesMasterGraph = nx.number_of_nodes(masterGraph)
    numberOfNodesWordGraph = nx.number_of_nodes(wordGraph)
    worksheet.write(row,1,numberOfNodesMasterGraph)
    worksheet.write(row,2,numberOfNodesWordGraph)
    result = False    
    if(numberOfNodesMasterGraph >= numberOfNodesWordGraph):
        result = True
    worksheet.write(row,3,result)

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
    print averageWordDegree
    worksheet.write(row,1,averageMasterDegree)
    worksheet.write(row,2,averageWordDegree)
    result = False    
    if(averageMasterDegree >= averageWordDegree):
        result = True
    worksheet.write(row,3,result)
    
    if result == True:
        return 1
    else:
        return -1
    
def compareAvgClusteringCoeff(masterGraph,wordGraph,worksheet,row):
    avgClusteringMaster = nx.average_clustering(masterGraph)
    avgClusteringWord = nx.average_clustering(wordGraph)
    worksheet.write(row,1,avgClusteringMaster)
    worksheet.write(row,2,avgClusteringWord)

    result = False    
    if(avgClusteringMaster >= avgClusteringWord):
        result = True
    worksheet.write(row,3,result)
    
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
    worksheet.write(row,1,averageNumberOfTrianglesMaster)
    worksheet.write(row,2,averageNumberOfTrianglesWord)

    result = False    
    if(averageNumberOfTrianglesMaster >= averageNumberOfTrianglesWord):
        result = True
    worksheet.write(row,3,result)
    
    if result == True:
        return 1
    else:
        return -1            

def compareLargestCC(masterGraph,wordGraph,worksheet,row):
    largestCCMaster = max(nx.connected_components(masterGraph))
    largestCCWord = max(nx.connected_components(wordGraph))
    worksheet.write(row,1,len(largestCCMaster))
    worksheet.write(row,2,len(largestCCWord))    

    result = False    
    if(len(largestCCMaster) >= len(largestCCWord)):
        result = True
    worksheet.write(row,3,result)
    
    if result == True:
        return 1
    else:
        return -1
    
def main():
    global name
    DG = pickle.load(open('directed_followers_graph.pkl','rb'))
    getWordGraph()
    filename = file("CompareResultsEdges.xlsx","wb")  
    workbook = xlsxwriter.Workbook(filename)
    bold = workbook.add_format({'bold': True})
    for value in wordGraph:        
        if value == '...':
            name = 'dotDotDot'
        else:
            name = value
        if value == '..':
            name = 'dotDot'
        else:
            name = value
        countNodes = 0        
        countDegree = 0
        countAvgClusteringCoeff = 0
        countAvgTriangles = 0
        countLargestCC = 0
        
        worksheet = workbook.add_worksheet(name)
        worksheet.set_column(0, 4, 30)
        worksheet.write(0,1,"Master Graph",bold)
        worksheet.write(0,2,"Word Graph",bold)
        worksheet.write(0,3," % Master Subgraphs > wordGraphs",bold)
        worksheet.write(0,4," % Master Subgraphs > wordGraphs",bold)
        worksheet.write(1,0,"Number Of Nodes",bold)        
        worksheet.write(2,0,"Average Degree",bold)
        worksheet.write(3,0,"Average Clustering Coefficient",bold)
        worksheet.write(4,0,"Average number of triangles",bold)
        worksheet.write(5,0,"Largest Connected Component",bold)
        #worksheet.write(6,0,"KCore",bold)
        #worksheet.write(7,0,"Graph",bold)
        graph =  wordGraph[value]
        undirectedGraph = graph.to_undirected()
        #nodes = nx.nodes(graph)
        numberOfEdges = nx.number_of_edges(graph)
        edges = DG.edges()
        row = 5
        for i in range(0,1000):
            worksheet.write(row + 1,0,"Random Subgraph #"+str(i+1),bold)
            worksheet.write(row + 2,0,"Number Of Nodes",bold)        
            worksheet.write(row + 3,0,"Average Degree",bold)
            worksheet.write(row + 4,0,"Average Clustering Coefficient",bold)
            worksheet.write(row + 5,0,"Average number of triangles",bold)
            worksheet.write(row + 6,0,"Largest Connected Component",bold)
            
            masterGraphEdges = random.sample(edges,numberOfEdges)
            masterGraph = nx.DiGraph(masterGraphEdges)
            undirectedMasterGraph = masterGraph.to_undirected()
            nodesResult = compareNumberOfNodes(undirectedMasterGraph,graph,worksheet,row + 2)
            if nodesResult == 1:
                countNodes = countNodes + 1
            degreeResult = compareAvgDegree(undirectedMasterGraph,graph,worksheet,row + 3)
            if degreeResult == 1:
                countDegree = countDegree + 1
            clusteringCoeffResult = compareAvgClusteringCoeff(undirectedMasterGraph,undirectedGraph,worksheet,row + 4)
            if clusteringCoeffResult == 1:
                countAvgClusteringCoeff = countAvgClusteringCoeff + 1
            numberOfTrianglesResult = compareAvgNumberOfTriangles(undirectedMasterGraph,undirectedGraph,worksheet,row + 5)
            if numberOfTrianglesResult == 1:
                countAvgTriangles = countAvgTriangles + 1
            LargestCCResult = compareLargestCC(undirectedMasterGraph,undirectedGraph,worksheet,row + 6)
            if LargestCCResult == 1:
                countLargestCC = countLargestCC + 1
            row = row + 6

        worksheet.write(1,1,countNodes,bold)
        worksheet.write(1,2,(1000 - countNodes),bold)
        worksheet.write(1,4,(countNodes/10),bold)
        worksheet.write(2,1,countDegree,bold)
        worksheet.write(2,2,(1000- countDegree),bold)
        worksheet.write(2,4,(countDegree/10),bold)
        worksheet.write(3,1,countAvgClusteringCoeff,bold)
        worksheet.write(3,2,(1000 - countAvgClusteringCoeff),bold)
        worksheet.write(3,4,(countAvgClusteringCoeff/10),bold)
        worksheet.write(4,1,countAvgTriangles,bold)
        worksheet.write(4,2,(1000 - countAvgTriangles),bold)
        worksheet.write(4,4,(countAvgTriangles/10),bold)
        worksheet.write(5,1,countLargestCC,bold)
        worksheet.write(5,2,(1000 - countLargestCC),bold)
        worksheet.write(5,4,(countLargestCC/10),bold)
    workbook.close()

if __name__ == "__main__":
    main()# -*- coding: utf-8 -*-