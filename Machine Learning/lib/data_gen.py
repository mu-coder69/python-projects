import numpy as np

def Lorenz63(init_val="random", sigma=10, rho=28, beta=8/3, size=10_000, discard=5_000):
    '''

    returns a numpy array sample of --size-- values

    dt = 0.005

    [ [x_values, y_values, z_values], [sigma], [rho], [beta] ]


    '''
    sigma = sigma
    rho = rho
    beta = beta
    discard = discard
    iterations = size + discard
    dt = 0.005

    if init_val == "random":

        x0 = np.round(np.random.uniform(0, 2),2)
        y0 = np.round(np.random.uniform(0, 2),2)
        z0 = np.round(np.random.uniform(0, 2),2)

    else:
        x0, y0, z0 = init_val
 
    ##----------funcion de Lorenz-63----------------------------

    def lorenz(v0):

        x, y, z = v0
        dx = sigma * (y - x) * dt
        dy = (x * (rho - z) - y) * dt
        dz = (x * y - beta * z) * dt

        return np.array([dx, dy, dz])

    #-----------Runge-Kutta 4------------------------

    def rk4(f, old_val):

        k1 = f(old_val)
        k2 = f(old_val + 0.5 * k1)
        k3 = f(old_val + 0.5 * k2)
        k4 = f(old_val + k3)

        new_val = old_val + (k1 + 2 * (k2 + k3) + k4) / 6

        return new_val

    ##---------------------------------------------------------

    val_list = np.zeros((3, size))

    val_list[:,0] = x0, y0, z0

    for i in range(discard):
        val_list[:,0] = rk4(lorenz, val_list[:,0])

    for i in range(iterations - discard -1):
        val_list[:,i+1] = rk4(lorenz, val_list[:,i])

    sigma = np.full((1, iterations - discard), sigma)
    rho = np.full((1, iterations - discard), rho)
    beta = np.full((1, iterations - discard), beta)

    data = np.concatenate((val_list, sigma, rho, beta), axis=0)
    
    return data

def gen_dataset(n_samples, x_lim, y_lim, separation=0.2):

    ## this give me a nice separation between groups
    a = np.random.uniform(-1.5, 2)
    b = -(abs(a +1) +2) * (a -1)
    coef = [a, b]

    f = lambda x: a * x + b

    data_a = np.array([])
    while data_a.shape[0] < int(n_samples / 2) * 3:

        x = np.random.uniform(x_lim[0], x_lim[1])
        y = np.random.uniform(y_lim[0], y_lim[1])
        if y >= f(x) + separation:
            coord = np.array([x, y, 1])
            data_a = np.append(data_a, coord)

    data_a = np.reshape(data_a, [-1, 3])

    data_b = np.array([])
    while data_b.shape[0] < int(n_samples / 2) * 3:

        x = np.random.uniform(x_lim[0], x_lim[1])
        y = np.random.uniform(y_lim[0], y_lim[1])
        if y <= f(x) - separation:
            coord = np.array([x, y, 0])
            data_b = np.append(data_b, coord, axis=0)
        
    data_b = np.reshape(data_b, [-1, 3])

    return data_a, data_b, coef

