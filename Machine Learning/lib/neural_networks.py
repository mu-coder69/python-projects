import numpy as np

## Perceptron functions and classes
class perceptron:

    def __init__(self, n_inputs, weights="random", bias=1):

        self.n_inputs = n_inputs
        self.weights = np.random.uniform(-1, 1, self.n_inputs) if weights == "random" else np.array(weights)
        self.bias = 1 if bias == 1 else bias
        self.accuracy = 0

    def feed(self, inputs):
        '''
        Recieve the inputs labeled, feed the perceptron and calculate the error of
        the network and its accuracy
        '''
        inputs_no_label = inputs[:, :-1]
        labels = inputs[:, -1]

        z = inputs_no_label * self.weights
        self.out = np.where(np.sum(z, 1) + self.bias > 0, 1, 0)

        self.error = labels - self.out

        self.accuracy = 100 - (1 - np.count_nonzero(self.error == 0)/self.error.size) * 100
        

    def train(self, lr, inputs, epochs):
        '''
        Train the network -epochs- times
        '''

        for epoch in range(epochs):
            self.feed(inputs)
            for i in range(self.error.size):
                for j in range(self.weights.size):
                    self.weights[j] += lr*self.error[i]*inputs[i, j]

        self.accuracy = 100 - (1 - np.count_nonzero(self.error == 0)/self.error.size) * 100






        