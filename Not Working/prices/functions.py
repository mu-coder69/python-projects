import numpy as np

def sortRows(matrixA, matrixB):
    '''
    sort the number of zeros in each row in ascending order
    '''
    zerosPerRow = np.count_nonzero(matrixA==0, axis=1)
    orderOfRows = np.argsort(zerosPerRow)
    rows = range(len(orderOfRows))

    matrixA[rows, :] = matrixA[orderOfRows, :] 
    matrixB[rows, :] = matrixB[orderOfRows, :] 

    return matrixA, matrixB

def sortColumns(matrix):
    '''
    sort the number of zeros in each column in descending order from right to left
    '''
    zerosPerColumn = np.count_nonzero(matrix==0, axis=0)
    orderOfColumns = np.argsort(zerosPerColumn)
    columns = range(len(orderOfColumns))

    matrix[:, columns] = matrix[:, orderOfColumns] 

    return matrix

def createPivot(matrix, pos):
    # fix
    # error when it doesn't find any good row
    row, column = pos
    totalColumns = matrix.shape[1]
    k = column +1
    while matrix[row, column] == 0:
        matrix[:, [column, k]] = matrix[:, [k, column]]

    matrix[row, :] /= matrix[row, column]
    return matrix

def reduce(matrix, adj):
    completeMatrix = np.concatenate((matrix, adj), axis=1)
    completeMatrix = completeMatrix[ np.any(completeMatrix != 0, axis=1)]
    totalRows, totalColumns = completeMatrix.shape

    # fix
    actualRow, actualColumn = 0, 0
    while completeMatrix[actualRow, :].any(): # while the actual row is not an empty row, do

        ## if the pivot is 0, search for a pivot, else divide the whole row 
        if completeMatrix[actualRow, actualColumn] == 0:
            completeMatrix = createPivot(completeMatrix, [actualRow, actualColumn])
        
        else: completeMatrix[actualRow, :] /= completeMatrix[actualRow, actualColumn]

        actualReducingRow = actualRow +1
        while completeMatrix[actualRow, :].any(): # while the actual reducing row is not an empty row, do
            completeMatrix[actualReducingRow, :] = completeMatrix[actualReducingRow, :] * completeMatrix[actualRow, actualColumn] - completeMatrix[actualRow, :] * completeMatrix[actualReducingRow, actualColumn]

            if not completeMatrix[actualReducingRow, :].any(): # if the actual reducing row is empty, delete it
                completeMatrix = np.delete(completeMatrix, actualReducingRow, axis=1)
                totalRows = completeMatrix.shape[0] # refresh the total rows number

            elif actualReducingRow < totalRows -1:
                actualReducingRow += 1
            else: break
        
        if actualRow < totalRows -1:
            actualRow +=1
            actualColumn +=1
        else: break
    # fix

    matrix = completeMatrix[:, :-1]
    adj = completeMatrix[:, -1].reshape((-1, 1))
    
    return matrix, adj

def isSquare(matrix):
    return matrix.shape[0] == matrix.shape[1]