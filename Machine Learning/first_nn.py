from lib import data_gen as dg, neural_networks as nn
import matplotlib.pyplot as plt
import numpy as np
import os

## create points sample
x_lim = y_lim = [0, 5] ## boundaries of the points
size = 300
sample_a, sample_b, coef = dg.gen_dataset(size, x_lim, y_lim)

## save the coef of the separator line
path = os.path.dirname(__file__)
for root, folder, _ in os.walk(path):
    if "data" in folder:
       path = os.path.join(root, "data")
       break
data_text_path = os.path.join(path, "line_coef.csv")
np.savetxt(data_text_path, coef, delimiter=", ")

## draw the line with the points
x = np.array(x_lim)
y = coef[0] * x + coef[1] 

plt.scatter(sample_a[:, 0], sample_a[:, 1], c="black")
plt.scatter(sample_b[:, 0], sample_b[:, 1], c="red")
plt.plot(x, y, "g")
plt.xlim(x_lim)
plt.ylim(y_lim)
plt.show()

## divide de sample data into training sample and test sample
train_to_test_ratio = 60 ## percentage
training_size = int(size * train_to_test_ratio/100)
test_size = size - training_size

training_sample = np.concatenate([sample_a[:int(training_size/2)], sample_b[:int(training_size/2)]])
testing_sample = np.concatenate([sample_a[-int(test_size/2):], sample_b[-int(test_size/2):]])




## create the NN
brain = nn.perceptron(2)

## first run and training
brain.feed(training_sample)
brain.train(0.03, training_sample, epochs=600)

## testing the network
brain.feed(testing_sample)
print(f"Perceptron accuracy: {round(brain.accuracy, 2)} %")




## save the weights for future use
path = os.path.dirname(__file__)
for root, folder, _ in os.walk(path):
    if "data" in folder:
        path = os.path.join(root, "data")
    break
data_text_path = os.path.join(path, "perceptron_weights.csv")
np.savetxt(data_text_path, brain.weights, delimiter=", ")
