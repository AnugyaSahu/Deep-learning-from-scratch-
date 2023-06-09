import numpy as np

import sys
sys.path.insert(0, r"C:\Users\anshu\OneDrive\Desktop\FAU\DL\exercise3_material\src_to_implement\Layers")
import Base, Helpers

class BatchNormalization(Base.BaseLayer):
    def __init__(self, channels):
        super(BatchNormalization, self).__init__()
        self.channels = channels
        self.trainable = True
        self.alpha = 0.8
        self.bias = np.zeros((channels))
        self.weights = np.ones((channels))
        self._gradient_bias = None
        self._gradient_weights = None
        self._optimizer = None
        self._bias_optimizer = None
        self.mean_test=None
        self.variance_test=None
    
    def initialize(self, weights_initializer=None, bias_initializer=None):
        self.bias = np.zeros((self.channels))
        self.weights = np.ones((self.channels))
        
    def reformat(self, tensor):
        
        if len(tensor.shape) == 4:
            self.shape_ = tensor.shape
            b, h, m, n = tensor.shape
            result = tensor.reshape((b, h, m*n))
            result = np.transpose(result, (0,2,1))
            result = result.reshape((b*m*n, h))
            return result
            
        if len(tensor.shape) == 2:
            b, h, m, n = self.shape_
            result = tensor.reshape((b, m*n, h))
            result = np.transpose(result, (0, 2, 1))
            result = result.reshape((b, h, m, n))
            return result
                
    
    def forward(self, input_tensor):
        eps = 10**(-15)
        temp = False
        if len(input_tensor.shape)==4:
            temp = True
            input_tensor = self.reformat(input_tensor)
        self.input_tensor = input_tensor
                    
        if self.testing_phase == False:
            self.mean = np.mean(input_tensor, axis=0)
            self.variance = np.var(input_tensor, axis=0)
            if self.mean_test is None or self.variance_test is None:
                self.mean_test = self.mean
                self.variance_test = self.variance
            else:
                self.mean_test = self.alpha*self.mean_test + (1 - self.alpha)*self.mean
                self.variance_test = self.alpha*self.variance_test + (1 - self.alpha)*self.variance
            self.X_hat = (input_tensor - self.mean)/np.sqrt(self.variance + eps)
                
        else:
            self.mean=self.mean_test
            self.variance=self.variance_test
            self.X_hat = (input_tensor - self.mean) / np.sqrt(self.variance + eps)
            
        output_tensor = self.weights*self.X_hat + self.bias
        
        if temp:
            output_tensor = self.reformat(output_tensor)
            
        return output_tensor
            
    
    def backward(self, error_tensor):
        
        temp = False
        if len(error_tensor.shape)==4:
            temp = True
            error_tensor = self.reformat(error_tensor)

        result = Helpers.compute_bn_gradients(error_tensor, self.input_tensor, self.weights, self.mean, self.variance, 1e-15)
        if temp:
            result = self.reformat(result)
        self.gradient_weights = np.sum(error_tensor * self.X_hat, axis=0)
        self.gradient_bias = np.sum(error_tensor, axis=0)
            
        if self.optimizer:
            self.weights = self.optimizer.calculate_update(self.weights, self.gradient_weights)
        if self.bias_optimizer:
            self.bias = self.bias_optimizer.calculate_update(self.bias, self.gradient_bias)
            
        return result
    
    @property
    def gradient_weights(self):
        return self._gradient_weights
    @gradient_weights.setter
    def gradient_weights(self, value):
        self._gradient_weights = value

    @property
    def gradient_bias(self):
        return self._gradient_bias
    @gradient_bias.setter
    def gradient_bias(self, value):
        self._gradient_bias = value

    @property
    def optimizer(self):
        return self._optimizer
    @optimizer.setter
    def optimizer(self, value):
        self._optimizer = value

    @property
    def bias_optimizer(self):
        return self._bias_optimizer
    @bias_optimizer.setter
    def bias_optimizer(self, value):
        self._bias_optimizer = value
