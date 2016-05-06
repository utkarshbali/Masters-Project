import xlrd
import xlsxwriter
import sys

worksheets = []
def main():
    global worksheets
    #fileName = 'CompareResultsMCMC.xlsx'
    fileName = sys.argv[1]
    outputFile = 'flattened' + fileName
    wb = xlsxwriter.Workbook(outputFile)
    workbook = xlrd.open_workbook(fileName)
    worksheets = workbook.sheet_names()
    ws = wb.add_worksheet('Results')
    bold = wb.add_format({'bold': True})
    print workbook.nsheets
    ws.set_column(0, 4, 30)    
    ws.write(0,0,"word",bold)
    ws.write(0,1,"Edges Count",bold)    
    ws.write(0,2,"Nodes Count",bold)
    ws.write(0,3,"Average Degree Count",bold)
    ws.write(0,4,"Average Clustering Coefficient Count",bold)
    ws.write(0,5,"Average number of triangles Count",bold)
    ws.write(0,6,"Largest Connected Component Count",bold)
    ws.write(0,7,"Overlap Count",bold)
    row = 0
    for name in worksheets:
        row = row + 1
        sheet = workbook.sheet_by_name(name)
        edges = sheet.cell(1,2)
        degree = sheet.cell(2,2)
        ccCount = sheet.cell(3,2)
        triangles = sheet.cell(4,2)
        connComp = sheet.cell(5,2)
        overlap = sheet.cell(6,2)
        ws.write(row,0,name)
        ws.write(row,1,edges.value)        
        ws.write(row,3,degree.value)
        ws.write(row,4,ccCount.value)
        ws.write(row,5,triangles.value)
        ws.write(row,6,connComp.value)
        ws.write(row,7,overlap.value)
    


if __name__ == "__main__":
    main()# -*- coding: utf-8 -*-


