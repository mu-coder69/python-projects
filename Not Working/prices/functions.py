import numpy as np

def isSquare(matrix):
    return matrix.shape[0] == matrix.shape[1]

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

def createPivot(matrix, pos):
    row, column = pos
    nonZero = np.nonzero(matrix[row:, column:])
    totalRows = matrix.shape[0]
    if row == totalRows -1: # if we are in the last row, just move the current column until the first non-zero element
        index = nonZero[0].tolist().index(row)
        column = nonZero[1, index]
        # while matrix[row, column] == 0:
        #     column += 1
    
    else: # else, we can search for a row to switch
        index = nonZero[1].tolist().index(column)
        k = nonZero[0, index]
        matrix[[row, k], :] = matrix[[k, row], :]

        k = row +1
        while matrix[row, column] == 0:
            matrix[[row, k], :] = matrix[[k, row], :]
        
            if k < totalRows-1:
                k +=1
            else: 
                column += 1
                k = row +1 

    # in any case, we can divide the whole row by the first non-zero element
    matrix[row, :] /= matrix[row, column]
    #then, return the matrix and the actual column
    return matrix, column

def reduce(matrix, adj):
    completeMatrix = np.concatenate((matrix, adj), axis=1)
    completeMatrix = completeMatrix[ np.any(completeMatrix != 0, axis=1)]
    totalRows, totalColumns = completeMatrix.shape

    # fix
    actualRow, actualColumn = 0, 0
    while completeMatrix[actualRow, :].any(): # while the actual row is not an empty row, do

        ## if the pivot is 0, search for a pivot, else divide the whole row 
        if completeMatrix[actualRow, actualColumn] == 0:
            completeMatrix, actualColumn = createPivot(completeMatrix, [actualRow, actualColumn])
        else: completeMatrix[actualRow, :] /= completeMatrix[actualRow, actualColumn]

        actualReducingRow = actualRow +1
        # while the actual reducing row is nither an empty row nor the last one, do
        while completeMatrix[actualRow, :].any() and actualReducingRow <= totalRows -1:
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
