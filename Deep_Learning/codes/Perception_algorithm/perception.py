import numpy as np
np.random.seed(42)
path = 'data.csv'
with open(path, encoding='utf-8') as f:
    data = np.loadtxt(path, delimiter=',')

W = np.array(np.random.rand(2, 1)) # 2x1 array
b = np.array(np.random.rand(1)) # 1x1 array
print(W, b)
print(data.T)