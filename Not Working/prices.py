'''
Trying to determinate prices of a purchase list only with the total prices and the qtty of items purchased

NOT WORKING
'''
import numpy as np
np.set_printoptions(precision=5, suppress=True)

# ------ initial conditions -----
costs = np.random.randint(low=1, high=100, size=(10, 1)) #random 10x1 costs matrix
purchases = np.zeros((5, 10)) # 5x10 zero matrix representing purchases
rows, columns = purchases.shape

# just half of the values in the purchases matrix has a value != 0 
# so i can test better the reduction algorithm
for i in range(int(rows * columns / 2)): 
    row = np.random.randint(0, 5)
    column = np.random.randint(0, 9)
    purchases[row, column] = np.random.randint(1, 10)

totals = np.around(purchases@costs, decimals=2) # total prices of each purchase

purchases[0] = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) # to test the sorting algorithm
totals[0] = purchases[0]@costs # refresh totals


# ----- format costs for user friendly display -------
for count, item in enumerate(costs):
    print(f"Product {count}: $ {item[0]}")


# ------ Gauss - Jordan elimination -----
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

def createPivot(matrix, pos):
    # fix
    # error when it doesn't find any good row
    row, column = pos
    totalRows = matrix.shape[0]
    k = row +1
    while matrix[row, column] == 0:
        matrix[[row, k], :] = matrix[[k, row], :]
        if k < totalRows -1:
            k += 1
        else:
            return matrix

    matrix[row, :] /= matrix[row, column]
    return matrix

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

try:
    costs = np.linalg.solve(purchases, totals) ## if the matrix is square, return the solutions
    print(costs)
except:
    incompleteMatrixRank = np.linalg.matrix_rank(purchases)
    completeMatrixRank = np.linalg.matrix_rank(np.concatenate((purchases, totals), axis=1))
    if incompleteMatrixRank == completeMatrixRank:
        print("The sistem can be solved")
        print(purchases)
        purchases, totals = sortRows(purchases, totals)
        # purchases = sortColumns(purchases)
        print(purchases)
        print(reduce(purchases, totals)[0])
        # print("purchases reduced")
        # print(purchases[np.any(purchases!=0, axis=1), np.any(purchases!=0, axis=0)]) # how do i store the deleted columns?
    else:
        print("I need more purchases lists")

'''
create the UI and test the program. Not sure if it's working properly.
'''