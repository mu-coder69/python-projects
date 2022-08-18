from lib import neural_networks as nn
import numpy as np


## AND gate 
brain = nn.perceptron(2, bias=-1)

data = [[0, 0, 0],
        [0, 1, 0],
        [1, 0, 0],
        [1, 1, 1]]

data = np.array(data)

brain.feed(data)
brain.train(0.5, data, epochs=600)

brain.feed(np.array([[0, 1, 0]]))
print(brain.out)