# Custom TransformerMixin to reshape data after oversampling
import numpy as np
import pandas as pd
from sklearn.base import TransformerMixin
from sklearn.utils import shuffle

class Reshape(TransformerMixin):

    def transform(self, X):
        return X.reshape(*X.shape, 1)

    def fit(self, X, y=None, **fit_params):
        return self
    
class SplitAndReshape(TransformerMixin):

    def transform(self, X):
        length = X.shape[1]//2
        X1 = X[:,:length]
        X2 = X[:, length:]
        return [X1.reshape(*X1.shape, 1), X2.reshape(*X2.shape, 1)]

    def fit(self, X, y=None, **fit_params):
        return self
    
class SplitAndReshape3(TransformerMixin):

    def transform(self, X):
        length = X.shape[1]//3
        X1 = X[:,:length]
        X2 = X[:, length:(2*length)]
        X3 = X[:, (2*length):]
        return [X1.reshape(*X1.shape, 1), X2.reshape(*X2.shape, 1), X3.reshape(*X3.shape, 1)]

    def fit(self, X, y=None, **fit_params):
        return self
    
# class LSTM_Reshape(TransformerMixin):
# Combine above?

    
class MultiTimeseriesReshape(TransformerMixin):
    
    def __init__(self, d=1):
        self.d = d
    
    def transform(self, X):
        return X.reshape(X.shape[0], X.shape[1]//self.d, self.d, order='F') 

    def fit(self, X, y=None, **fit_params):
        return self

class DataFrameReshape(TransformerMixin):
    
    def __init__(self, d=1):
        self.d = d
    
    def transform(self, X):
        cols = []
        for i in range(self.d):
            df = pd.DataFrame(X)
            cols.append(pd.DataFrame(df.apply(lambda row: np.array(row),axis=1), columns=[i]))
        if self.d == 1:
            return cols[0]
  
        return pd.concat(cols, axis=1)
     
    def fit(self, X, y=None, **fit_params):
        return self
    
    