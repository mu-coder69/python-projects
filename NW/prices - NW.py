'''
Trying to determinate prices of a purchase list only with the total prices and the qtty of items purchased

NOT WORKING
'''

from re import I
import numpy as np

# ------ initial conditions -----
costs = np.random.randint(100, size=(10, 1))
purchases = np.zeros((5, 10))
for i in range(int(purchases.shape[0] * purchases.shape[1] / 2)):
    purchases[np.random.randint(0, 5), np.random.randint(0, 10)] = np.random.randint(0, 10)
totals = np.around(purchases@costs, decimals=2)

purchases[0] = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
# purchases[1] = np.array([0, 0, 0, 0, 0, 4, 5, 0, 0, 0])
totals[0] = purchases[0]@costs
# totals[1] = purchases[1]@costs



# ----- format costs for user friendly display -------
for count, item in enumerate(costs):
    print(f"Product {count}: $ {item[0]}")


# ------ Gauss - Jordan elimination -----
def reduce(matrix, adj):
    extMatrix = np.concatenate((matrix, adj), axis=1)

    for i in range(0, extMatrix.shape[0]):

        ## making sure the first element of the current row is not 0. If all 0, then swap to the last row
        k = 1
        while extMatrix[i, i] == 0:
            try:
                extMatrix[:, [i, i +k]] = extMatrix[:, [i +k, i]]
                k += 1
            except:
                extMatrix[[-1, i]] = extMatrix[[i, -1]]
                k = 1

        for j in range(i+1, extMatrix.shape[0]):
            if extMatrix[j, i] != 0:
                extMatrix[j, :] = extMatrix[j, i] * extMatrix[i, :] - extMatrix[i, i] * extMatrix[j, :]

        ## divide the whole row by its first coeff
        # extMatrix[i, :] /= extMatrix[i, i]

        # print(extMatrix)    
        # extMatrix = np.concatenate(sort(extMatrix[:, :-1], extMatrix[:, -1].reshape((-1, 1))), axis=1)
        # print("post sort", extMatrix, sep="\n")

    matrix = extMatrix[:, :-1]
    adj = extMatrix[:, -1].reshape((-1, 1))
    
    return matrix, adj

def countZeros(matrix):
    zerosPerRow = {}
    
    for i, row in enumerate(matrix):
        zeros = 0 
        for elem in row:
            if elem == 0: zeros += 1

        zerosPerRow[i] = zeros
    
    return dict(sorted(zerosPerRow.items(), key=lambda item: item[1]))  

def sort(matrixA, matrixB):
    '''
    sort the number of zeros in each row vertically in ascending order
    '''
    order = countZeros(matrixA)

    newMatrixA = np.zeros_like(matrixA)
    newMatrixB = np.zeros_like(matrixB)

    for i, row in enumerate(order):
        newMatrixA[i] = matrixA[row]
        newMatrixB[i] = matrixB[row]

    for i in range(matrixA.shape[1]):
        for j in range(i, matrixA.shape[1]):
            if not newMatrixA[:, i].any() and not newMatrixA[:, j].any(): newMatrixA[:, [i, j]] = newMatrixA[:, [j, i]]
    
    return newMatrixA, newMatrixB

def usefull(matrix):
    rows, columns = matrix.shape
    
    null = []
    for i in range(rows):
        if not matrix[i].any(): null.append(i)
    matrix = np.delete(matrix, null, axis=0)

    # null = []
    # for i in range(columns):
    #     if not matrix[:, i].any(): null.append(i)
    # matrix = np.delete(matrix, null, axis=1)

    return matrix

# def attempt(matrixA, matrixB):
#     shape = matrixA.shape

#     for i in range(0, shape[0], -1):
#         try:
#             costs = np.linalg.solve(matrixA[i, i], matrixB[i])


try:
    costs = np.linalg.solve(purchases, totals) ## if the matrix is square, return the solutions
    print(costs)
except:
    print("---original purchases---")
    print(purchases)
    print("---sorted purchases and total---")
    purchases, totals = sort(purchases, totals)
    print(purchases, totals, sep="\n")
    print("---getting rid of empy rows and columns---")
    purchases, totals = usefull(purchases), usefull(totals)
    print("---cleaned purchases and totals---")
    print(purchases, totals, sep="\n")
    print("---reducing matrices---")
    purchasesRed, totalsRed = reduce(purchases, totals)
    print("purchasesRed:", np.around(purchasesRed, 2), sep="\n")
    print("totalsRed:", totalsRed, sep="\n")
    purchasesRed, totalsRed = usefull(purchasesRed), usefull(totalsRed)
    print("---final cleaned matrices---")
    print("purchasesRed:", np.around(purchasesRed, 2), sep="\n")
    print("totalsRed:", totalsRed, sep="\n")

    
# for row in reduce(purchases, totals):
#     print([round(el, 2) for el in row.tolist()])


'''
create the UI and test the program. Not sure if it's working properly.
'''