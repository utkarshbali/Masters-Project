import random
import pickle
import networkx as nx
import numpy as np
import xlsxwriter
import mcmc

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
    
def compare_intersection(masterGraph, workgraph, expected_overlap, worksheet, row):
    overlap = len(set(masterGraph.nodes_iter()) & set(workgraph.nodes_iter()))
    worksheet.write(row,1,expected_overlap)
    worksheet.write(row,2,overlap)
    if  overlap <= expected_overlap:
        worksheet.write(row,3,True)
        return 1
    else:
        worksheet.write(row,3,False)
        return -1

def main():
    global name
    DG = pickle.load(open('/usr/space1/uvb6476/directed_followers_graph.pkl','rb'))
    getWordGraph('/usr/space1/uvb6476/wordGraph_500.pkl')
    filename = file("CompareResultsMCMC500.xlsx","wb")
    workbook = xlsxwriter.Workbook(filename, {'nan_inf_to_errors': True})
    bold = workbook.add_format({'bold': True})
    UG = DG.to_undirected()
    nodes = UG.nodes()
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
        countOverlap = 0

        try:
            worksheet = workbook.add_worksheet(name)
            worksheet.set_column(0, 4, 30)
            worksheet.write(0,1,"Master Graph",bold)
            worksheet.write(0,2,"Word Graph",bold)
            worksheet.write(0,3," % Master Subgraphs > wordGraphs",bold)
            worksheet.write(0,4," % Master Subgraphs > wordGraphs",bold)
            worksheet.write(1,0,"Number Of Nodes",bold)
            worksheet.write(2,0,"Number Of Edges",bold)
            worksheet.write(3,0,"Average Degree",bold)
            worksheet.write(4,0,"Average Clustering Coefficient",bold)
            worksheet.write(5,0,"Average number of triangles",bold)
            worksheet.write(6,0,"Largest Connected Component",bold)
            worksheet.write(7,0,"Overlap",bold)

            
            #worksheet.write(6,0,"KCore",bold)
            #worksheet.write(7,0,"Graph",bold)
            graph =  wordGraph[value]
            undirectedGraph = graph.to_undirected()
            numberOfNodes =  nx.number_of_nodes(undirectedGraph) 
            #print numberOfNodes
            #print nx.number_of_edges(undirectedGraph)
            expected_overlap = numberOfNodes * numberOfNodes / len(nodes)
            row = 7
            for i in range(0,1000):
                worksheet.write(row + 1,0,"Random Subgraph #"+str(i+1),bold)
                worksheet.write(row + 2,0,"Number Of Edges",bold)
                worksheet.write(row + 3,0,"Average Degree",bold)
                worksheet.write(row + 4,0,"Average Clustering Coefficient",bold)
                worksheet.write(row + 5,0,"Average number of triangles",bold)
                worksheet.write(row + 6,0,"Largest Connected Component",bold)
                worksheet.write(row + 7,0,"Overlap",bold)

    	       
                masterGraphNodes = mcmc.mcmc_subgraph_sample(UG, undirectedGraph)
                undirectedMasterGraph = UG.subgraph(masterGraphNodes)
                if nx.number_of_nodes(undirectedGraph) > 0:
                    nodesResult = compareNumberOfEdges(undirectedMasterGraph,graph,worksheet,row + 2)
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
                    overlap = compare_intersection(undirectedMasterGraph, undirectedGraph, expected_overlap, worksheet, row+7)
                    if overlap == 1:
                        countOverlap += 1
                else:
                    worksheet.write(row + 1,1,"0",bold)
                    worksheet.write(row + 2,1,"0",bold)
                    worksheet.write(row + 3,1,"0",bold)
                    worksheet.write(row + 4,1,"0",bold)
                    worksheet.write(row + 5,1,"0",bold)
                    worksheet.write(row + 6,1,"0",bold)
                    worksheet.write(row + 7,1,"0",bold)
                   
                row = row + 7
                
            
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
            worksheet.write(6,1,countOverlap,bold)
            worksheet.write(6,2,(1000 - countOverlap),bold)
            worksheet.write(6,4,(countOverlap/10),bold)
        except Exception as e:
            print e
            print name
        
    workbook.close()

if __name__ == "__main__":
    main()# -*- coding: utf-8 -*-
