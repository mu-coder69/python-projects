'''
Trying to determinate prices of a purchase list only with the total prices and the qtty of items purchased

NOT WORKING
'''
import numpy as np
from functions import *
np.set_printoptions(precision=5, suppress=True)

# ------ INITIAL CONDITIONS -----
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
# ------ INITIAL CONDITIONS -----


# ----- FORMAT COSTS FOR USER FRIENDLY DISPLAY -------
for count, item in enumerate(costs):
    print(f"Product {count}: $ {item[0]}")
# ----- FORMAT COSTS FOR USER FRIENDLY DISPLAY -------



if isSquare(purchases):
    costs = np.linalg.solve(purchases, totals) ## if the matrix is square, return the solutions
    print(costs)
else:
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