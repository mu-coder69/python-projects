
import numpy as np
import matplotlib.pyplot as plt

x = np.random.randint(-20, 21, (21, 21))

# Hacer una libreria de transformacion de matrices

def transform(matrix):

    matrix = np.reshape(matrix, 9)
    sum_ = 0 if np.sum(matrix) <= 0 else np.sum(matrix)
    trans_matrix = [[0*matrix[0], 0*matrix[1] , 0*matrix[2]],
                    [0*matrix[3], sum_ , 0*matrix[5]],
                    [0*matrix[6], 0*matrix[7] , 0*matrix[8]]]

    trans_matrix = np.array(trans_matrix)
    return  trans_matrix

def local_matrix(x, pos):
    r, c = pos

    matrix = np.zeros((3, 3), dtype=int)
    for i in range(-1, 2, 1):
        for j in range(-1, 2, 1):
            matrix[1 +i, 1 +j] = x[r +i, c +j]

    return matrix

def change_matrix(x, y, pos):

    r, c = pos
    x[r, c] = y[1,1]
    # for i in range(-1, 2, 1):
    #     for j in range(-1, 2, 1):
    
    return x

# graph1 = plt.subplot(1, 2, 1)
im1 = plt.imshow(x, cmap="plasma")
plt.colorbar(im1,fraction=0.046, pad=0.04)

y = np.zeros((x.shape[0], x.shape[1]))
for i in range(1, x.shape[0] -1, 3):  # rows
    for j in range(1, x.shape[1] -1, 3):  #column

        loc = local_matrix(x, (i, j))
        new_loc = transform(loc)
        change_matrix(y, new_loc, (i, j))

for i in range(1, x.shape[0] -1, 3):  # rows
    for j in range(1, x.shape[1] -1, 3):  #column

        x[i, j] = y[i, j]

print(x)
# print(y)
# graph2 = plt.subplot(1, 2, 2)
# im2 = plt.imshow(y, cmap="binary_r")
# plt.colorbar(im2,fraction=0.046, pad=0.04)
plt.tight_layout()
plt.show()
