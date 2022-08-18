import numpy as np
import numpy.random as rnd
import matplotlib.pyplot as plt
import torch
from torch.autograd import Variable
import torch.nn.functional as F
from torch.utils.data import Dataset
from torch.utils import data 
 

def customLoss(dataout, obs):
    # Return MSE loss 
    return F.mse_loss(dataout, obs)

Loss = customLoss
n_samples=10000
n_val = 500
batch_size = 64
n_epochs = 60

# Generate some  data
def fn_noise(x):
    return np.sin(x*2*np.pi)

def fn_regr(x):
    return np.abs(np.sin(10*x)/3)

def sample(n_samples):
    # Genero input output data
    x = rnd.random(n_samples)
    eps = rnd.normal(scale=1.0, size=n_samples) *fn_noise(x)
    y =  fn_regr(x)+ eps

    y=np.reshape(y,(n_samples, 1))
    x=np.reshape(x,(n_samples, 1))
    return x,y


# Object to generate dataset suitable for DataLoader
class DriveData(Dataset):
    "para utilizarse con el DataLoader de pytorch "
    def __init__(self,transform=None,n_samples=10000):
        self.xs,self.ys=sample(n_samples)
        self.x_data = torch.from_numpy(np.asarray(self.xs,dtype=np.float32))
        self.y_data = torch.from_numpy(np.asarray(self.ys,dtype=np.float32))
        self.lenx= len(self.xs)
        
    def __getitem__(self,index):
        return self.x_data[index], self.y_data[index]
    
    def __len__(self):
        return self.lenx
    def getnp(self):
        return self.xs, self.ys


## training sample -------------------------------------
# Generate training dataset 
dset_train = DriveData(n_samples=n_samples)
loader_train = data.DataLoader(dset_train, batch_size=batch_size,shuffle=True)


## testing sample -------------------------------------
# validation dataset
dset_val = DriveData(n_samples=n_val)
loader_val = data.DataLoader(dset_val, batch_size=n_val)


## create the net --------------------------------------
# Create a simple two-layer network with one input (x) and two outputs (y, sigma)
n_inputs  = 1 # mean
n_outputs = 1 # predict mean    
n_hidden = 1000

## 1
## 1000
## 1

model = torch.nn.Sequential(torch.nn.Linear(n_inputs, n_hidden),
                            torch.nn.ReLU(),
                            torch.nn.Linear(n_hidden, n_outputs))

## optimice the net ----------------------------
# Adam optimizer
learning_rate = 1e-3
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

# training loop. We train this simple model with batch size equal to the whole dataset.
for iepoch in range(n_epochs):
    # Calculate predicted y from x
    for local_batch, local_labels in loader_train:
    
        y_f = model(local_batch)
    
        # Calculate loss
        loss = Loss(y_f, local_labels)
        #if iepoch%500 == 0: print(f'epoch: {iepoch:4}, loss: {loss.data:.3}',)

        # Backprop, first zeroing gradients
        optimizer.zero_grad() # inicializo las variables adjuntas
        
        loss.backward()

        # Update parameters
        optimizer.step()

# Get predicted y and its predicted variance for validation set
for x_val, y_val in loader_val:    
    y_f = model(x_val)
    mean_f = y_f[:,0].cpu().data
#    var_f = y_f[:,1].cpu().data
    
print ('Termina validation')

# Plot the data
#x,y=dset_train.getnp()
#plt.figure(figsize=(14,6))
#plt.plot(x, y[:,0], '.')
#plt.xlabel(r'$x$')
#plt.ylabel(r'$y$')
#plt.savefig('tmp/fig1.png')

# Plot predictions and their errors
xs = np.linspace(0.0, 1.0, 50)
# err = fn_noise(xs)
plt.figure(figsize=(14,6))
#plt.errorbar(x_val, mean_f, yerr=var_f.sqrt() , fmt='.')
#plt.errorbar(x_val, mean_f, yerr=var_f , fmt='.')
plt.plot(x_val, mean_f,'.')
#plt.fill_between(xs, fn_regr(xs)-err, fn_regr(xs)+err, facecolor='orange',  alpha=0.5);
plt.plot(xs,fn_regr(xs))
plt.xlabel('x');
plt.ylabel('y');
plt.legend(['Predicciones','Datos'], loc='upper left');
#plt.savefig('tmp/fig2.png')
plt.show()
