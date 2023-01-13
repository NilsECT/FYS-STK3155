from random import seed
import numpy as np


def GD(X, y, n_iter, eta0, optimization=None, lmbda=0, gamma=0, eps=1e-10):
    
    """
    X: Design matrix
    y: Response data
    n_iter: number of iterations
    eta0: initial learning rate 
    rate: Choose an optimization method for the learning rate. Default is a constant learning rate. 
    Options are:
        - adagrad
    lmbda: Regularization term, if zero we do OLS regression, if lmbda > 0 we do Ridge regression
    gamma: Momentum term. If zero, we use gradient descent without momentum, if gamma > 0 we use momentum.
        - Suggested value: 0.5, 0.9 or 0.99 (ch. 8 Goodfellow)
    eps: Tolerance for gradient. If norm of gradient is very small, stop gradient descent algorithm.
    """
    
    p = X.shape[1] # num features
    N = X.shape[0]  # num data points
    beta = np.random.randn(p, 1) # randomly initiate beta
    
    eta = eta0 # learning rate 
    change = np.zeros_like(beta) # Initiate the values with which beta changes
    
    delta = 1e-8 # to avoid division by zero
    r = np.zeros(shape=(p,p))

    for i in range(n_iter):

        gradient = 2.0 / N * X.T @ (X @ beta - y) + 2.0 * lmbda * beta # if lambda>0, we do Ridge regression
        
        if optimization is None:
            change = -eta*gradient + gamma*change

        elif optimization == "adagrad":
            r += gradient @ gradient.T
            scale = np.c_[1.0 / (delta + np.sqrt(np.diagonal(r)))]
            change = -eta*np.multiply(scale, gradient) + gamma*change

        change = -eta*np.multiply(scale, gradient) + gamma*change
        beta += change

        if(np.linalg.norm(gradient) <= eps): #stop iterating once it has converged sufficiently
            print(f"Stopped after {i} iterations.")
            break

    return beta

def SGD(X, y, n_epochs, eta0, optimization, M=1, lmbda=0, gamma=0, eps=1e-8):
    """
    X: Design matrix
    y: Response data
    n_epochs: number of epochs
    rate: Choose an optimization method for the learning rate. Default is a constant learning rate. 
    Options are:
        - constant
        - adagrad
        - RMSprop
        - adam
    M: minibatch size
    lmbda: Regularization term, if zero we do OLS regression
    gamma: Momentum term, if zero we use SDG without momentum
    eps: Tolerance for gradient (if very small, stop gradient descent)
    """
    p = X.shape[1] # num. features
    N = X.shape[0] # num. data points

    m = int(N/M) # num. batches

    beta = np.random.randn(p, 1) #initialize beta
    delta = 1e-8 # to avoid division by zero

    def learning_schedule(t, eta):
        alpha = t / (n_epochs*m)
        return (1-alpha) * eta0 + alpha * eta

    rho1 = 0.9 # optimization decay values, based on suggested default in Goodfellow, might make tunable 
    rho2 = 0.999

    change = np.zeros_like(beta) # initiate vector used for computing change in beta
    eta = eta0

    for epoch in range(1, n_epochs+1):
        #Giter = np.zeros(shape=(p,p))
        s = np.zeros_like(beta)
        r = np.zeros(shape=(p,p))

        for i in range(m):
            random_index = M*np.random.randint(m)
            Xk = X[random_index:random_index+M] # ideally want to shuffle data before this
            yk = y[random_index:random_index+M]

            #Compute the gradient using the data in minibatch k
            gradient = 2.0/M * Xk.T @ (Xk @ beta - yk) + 2.0 * lmbda * beta
            eta = learning_schedule(t = epoch * m + i, eta = eta)

            if optimization is None:
                change = -eta*gradient + gamma*change

            elif optimization == "adagrad":
                r = r + gradient @ gradient.T # sum of squared gradients
                rr = np.diagonal(r) # we want g_i**2
                scale = np.c_[1 / (delta + np.sqrt(rr))]
                change = -eta*np.multiply(scale, gradient) + gamma*change # scale gradient element-wise

            elif optimization == "RMSprop":
                # Previous = Giter
                # Giter += gradient @ gradient.T
                # Gnew = decay*Previous + (1-decay) * Giter
                # scale = np.c_[ 1.0 / (delta + np.sqrt(np.diagonal(Gnew)))]
                # change = -eta0*np.multiply(scale, gradient) + gamma*change
                
                r = rho1 * r + (1 - rho1) * gradient @ gradient.T
                rr = np.c_[np.diagonal(r)]
                scale = np.c_[1.0 / (delta + np.sqrt(rr))]
                change = -eta*np.multiply(scale, gradient) # scale gradient element-wise
            
            elif optimization == "adam":
                t = i+1 # iteration number
                #here we compute 1st and 2nd moments
                r = rho2*r + (1-rho2) * gradient @ gradient.T    
                s = rho1*s + (1-rho1) * gradient 
                
                ss = s/(1 - rho1**t) # here we correct the bias
                rr = np.c_[np.diagonal(r)/(1 - rho2**t)]
                
                change = np.c_[ -eta * ss / (delta + np.sqrt(rr))] 
            
            beta += change
    # what is the ideal stopping criterion?    
    return beta
