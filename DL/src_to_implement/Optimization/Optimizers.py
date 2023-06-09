import numpy as np

class Optimizer:
    def __init__(self):
        self.regularizer = None

    def add_regularizer(self, value):
        self.regularizer = value
        
class Sgd(Optimizer):
    def __init__(self, learning_rate):
        super(Sgd, self).__init__()
        self.learning_rate = learning_rate
    
    def calculate_update(self, weight_tensor, gradient_tensor):
        
        if self.regularizer:
            reg = self.regularizer.calculate_gradient(weight_tensor)
            weight_tensor = weight_tensor - self.learning_rate * reg
            
        weight_tensor1 = weight_tensor - self.learning_rate*gradient_tensor
        return weight_tensor1
    
class SgdWithMomentum(Optimizer):
    def __init__(self, learning_rate, momentum_rate):
        super(SgdWithMomentum, self).__init__()
        self.learning_rate = learning_rate
        self.momentum_rate = momentum_rate
        self.v_k = 0
        
    def calculate_update(self, weight_tensor, gradient_tensor):
        
        if self.regularizer:
            reg = self.regularizer.calculate_gradient(weight_tensor)
            weight_tensor = weight_tensor - self.learning_rate * reg
            
        self.v_k = self.momentum_rate*self.v_k - self.learning_rate*gradient_tensor
        weight_tensor1 = weight_tensor + self.v_k
        return weight_tensor1

class Adam(Optimizer):
    def __init__(self, learning_rate, mu, rho):
        super(Adam, self).__init__()
        self.learning_rate = learning_rate
        self.mu, self.rho = mu, rho
        self.v_k, self.r_k = 0, 0
        self.v_hat_k, self.r_hat_k = 0, 0
        self.k = 1
    
    def calculate_update(self, weight_tensor, gradient_tensor):
        
        if self.regularizer:
            reg = self.regularizer.calculate_gradient(weight_tensor)
            weight_tensor = weight_tensor - self.learning_rate * reg
            
        self.v_k = self.mu*self.v_k + (1 - self.mu)*gradient_tensor
        self.r_k = self.rho*self.r_k + (1 - self.rho)*gradient_tensor*gradient_tensor
        self.v_hat_k = self.v_k/(1 - self.mu**self.k)
        self.r_hat_k = self.r_k/(1 - self.rho**self.k)
        self.k += 1
        weight_tensor1 = weight_tensor - self.learning_rate*(self.v_hat_k/(np.sqrt(self.r_hat_k)+np.finfo(float).eps))
        return weight_tensor1
