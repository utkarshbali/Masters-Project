import random
import pickle
import networkx as nx
import numpy as np
import xlsxwriter

wordGraph = {}
name = ''

def getWordGraph(filename):
    global wordGraph
    wordGraph = pickle.load(open(filename,"rb"))

def compareNumberOfEdges(masterGraph,wordGraph,worksheet,row):
    numberOfEdgesMasterGraph = nx.number_of_edges(masterGraph)
    numberOfEdgesWordGraph = nx.number_of_edges(wordGraph)
    worksheet.write(row,1,numberOfEdgesMasterGraph)
    worksheet.write(row,2,numberOfEdgesWordGraph)
    result = False
    if(numberOfEdgesMasterGraph >= numberOfEdgesWordGraph):
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
    DG = pickle.load(open('/usr/space1/uvb6476/directed_followers_graph.pkl','rb'))
    getWordGraph('/usr/space1/uvb6476/wordGraph_mid.pkl','rb')
    filename = file("CompareResultsNodes.xlsx","wb")
    workbook = xlsxwriter.Workbook(filename)
    bold = workbook.add_format({'bold': True})
    for value in wordGraph:
        if value == '...':
            name = 'dotDotDot'
        else:
            name = value
        countNodes = 0
        countDegree = 0
        countAvgClusteringCoeff = 0
        countAvgTriangles = 0
        countLargestCC = 0
        
        
        #worksheet.write(6,0,"KCore",bold)
        #worksheet.write(7,0,"Graph",bold)
        graph =  wordGraph[value]
        undirectedGraph = graph.to_undirected()
        UG = DG.to_undirected()
        
        print nx.number_of_edges(undirectedGraph)
        row = 5
        for i in range(0,1000):
            
            masterGraphNodes = mcmc_subgraph_sample(UG, undiredctedGraph)
            masterGraph = UG.subgraph(masterGraphNodes)
            print nx.number_of_edges(masterGraph)
            
        '''
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
        '''
    #workbook.close()

if __name__ == "__main__":
    main()# -*- coding: utf-8 -*-