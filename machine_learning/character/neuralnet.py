# coding:utf8
import numpy as np
import sys

def expit(x):

    z =  .5  * x
    np.tanh(z,z) # 双曲正切函数
    z += 1
    z *=  .5
    return z

class NeuralNetMLP:

    def __init__(self,n_output,n_features,n_hidden=30,l1=0.0,l2=0.0,epochs =500,eta=0.001,alpha=0.0,decrease_const=0.0,shuffle=True,minibatches=1,random_state=None):
        np.random.seed(random_state)
        self.n_output = n_output
        self.n_feature = n_features
        self.n_hidden = n_hidden
        self.w1,self.w2 = self._initialize_weights()
        self.l1 = l1
        self.l2 = l2
        self.epochs = epochs
        self.eta = eta
        self.alpha = alpha
        self.decrease_cost = decrease_const
        self.shuffle = shuffle
        self.minibatches = minibatches

    def _encode_labels(self,y,k):
        onehot = np.zeros((k,y.shape[0]))
        for idx,val in enumerate(y):
            onehot[val,idx] = 1.0
        return onehot

    def _initialize_weights(self):
        w1 = np.random.uniform(-1.0,1.0,size=self.n_hidden*(self.n_feature+1))
        w1 = w1.reshape(self.n_hidden,self.n_feature+1)
        w2 = np.random.uniform(-1.0,1.0,size=self.n_output*(self.n_hidden+1))
        w2 = w2.reshape(self.n_output,self.n_hidden+1)
        return w1,w2

    def _sigmoid(self,z):
        '''expit is equivalent to 1.0/(1.0+np.exp(-z))'''
        return expit(z)

    def _sigmoid_gradient(self,z):
        sg = self._sigmoid(z)
        return sg*(1-sg)

    def _add_bias_unit(self,X,how='column'):
        if how=='column':
            X_new = np.ones((X.shape[0],X.shape[1]+1))
            X_new[:,1:] = X
        elif how == "row":
            X_new = np.ones((X.shape[0]+1,X.shape[1]))
            X_new[1:,:] = X
        else:
            raise AttributeError('how参数错误')
        return X_new

    def _feedforward(self,X,w1,w2):
        a1 = self._add_bias_unit(X,how='column')
        z2 = w1.dot(a1.T)
        a2 = self._sigmoid(z2)
        a2 = self._add_bias_unit(a2,how='row')
        z3 = w2.dot(a2)
        a3 = self._sigmoid(z3)
        return a1,z2,a2,z3,a3

    def _L2_reg(self,lambda_,w1,w2):
        return (lambda_/2.0)*(np.sum(w1[:,1:]**2)+np.sum(w2[:,1:]**2))

    def _L1_reg(self,lambda_,w1,w2):
        return (lambda_/2.0)*(np.abs(w1[:,1:]).sum()+np.abs(w2[:,1:]).sum())

    def _get_cost(self):
        cost = 1+2
        return cost

    def predict(self,y_enc,output,w1,w2):
        term1 = -y_enc*(np.log(output))
        term2 = (1-y_enc)*np.log(1-output)
        cost = np.sum(term1-term2)
        L1_term = self._L1_reg(self.l1,w1,w2)
        L2_term = self._L2_reg(self.l2,w1,w2)
        cost = cost + L1_term + L2_term
        return cost

    def _get_gradient(self,a1,a2,a3,z2,y_enc,w1,w2):
        sigma3 = a3 - y_enc
        z2 = self._add_bias_unit(z2,how='row')
        sigma2 = w2.T.dot(sigma3) * self._sigmoid_gradient(z2)
        sigma2 = sigma2[1:,:]
        grad1 = sigma2.dot(a1)
        grad2 = sigma3.dot(a2.T)

        # regularize
        grad1[:,1:] += (w1[:,1:] * (self.l1 + self.l2))
        grad2[:,1:] += (w2[:,1:] * (self.l1 + self.l2))

    def fit(self,X,y,print_progress=False):
        self.cost_ = []
        return self


