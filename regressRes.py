import xlrd
from sklearn import linear_model
import sys
import matplotlib.pyplot as plt
import numpy as np

wordsDict = {}

def main():
    global wordsDict
    fileName = 'flattenedCompareResultsMCMC200.xlsx'
    #fileName = 'flattenedlabeled.xlsx'
    #fileName = sys.argv[1]
    workbook = xlrd.open_workbook(fileName)
    worksheets = workbook.sheet_names()
    for worksheet in worksheets:
        sheet = workbook.sheet_by_name(worksheet)
        rows = sheet.nrows
        averageDegreeCount = []
        avgClusteringCoeff = []
        avgNumTriangles = []
        largestConnComp = []
        overlapCount = []
        label = []
        data = []
        for i in range(1,rows):
            if(sheet.cell_type(i,8) != 0):
                averageDegreeCount.append(sheet.cell(i,3).value)
                avgClusteringCoeff.append(sheet.cell(i,4).value)
                avgNumTriangles.append(sheet.cell(i,5).value)
                largestConnComp.append(sheet.cell(i,6).value)
                overlapCount.append(sheet.cell(i,7).value)
                label.append(sheet.cell(i,8).value)
        for i in range(0,len(label)):
            values = [averageDegreeCount[i],avgClusteringCoeff[i],avgNumTriangles[i],largestConnComp[i],overlapCount[i]]
            data.append(values)
        
        data = np.array(data)
        label = np.array(label)
        wordsDict = {'data': data,'target': label}
        
        # Use only one feature
        wordsDict_X = wordsDict['data']
        # Split the data into training/testing sets
        wordsDict_X_train = wordsDict_X[:-20]
        wordsDict_X_test = wordsDict_X[-20:]
        
        # Split the targets into training/testing sets
        wordsDict_y_train = wordsDict['target'][:-20]
        wordsDict_y_test = wordsDict['target'][-20:]
        
        # Create linear regression object
        regr = linear_model.LinearRegression()
        
        # Train the model using the training sets
        regr.fit(wordsDict_X_train, wordsDict_y_train)
        
        # The coefficients
        print('Coefficients: \n', regr.coef_)
        # The mean square error
        print("Residual sum of squares: %.2f"
              % np.mean((regr.predict(wordsDict_X_test) - wordsDict_y_test) ** 2))
        # Explained variance score: 1 is perfect prediction
        print('Variance score: %.2f' % regr.score(wordsDict_X_test, wordsDict_y_test))
        predictedScores = regr.predict(wordsDict_X_test)
        
        for i in range(0,len(wordsDict_y_test)):
            plt.plot(wordsDict_y_test[i],predictedScores[i],"o")

        plt.axis([0,6,0,6])
        plt.xlabel("Label")
        plt.ylabel("Regression Score")
        plt.savefig('results.eps', format='eps', dpi=1000)
        plt.show()
#        # Plot outputs
#        plt.scatter(wordsDict_X_test, wordsDict_y_test,  color='black')
#        plt.plot(wordsDict_X_test, regr.predict(wordsDict_X_test), color='blue',
#                 linewidth=3)
#        
#        plt.xticks(())
#        plt.yticks(())
#        plt.show()

if __name__ == "__main__":
    main()