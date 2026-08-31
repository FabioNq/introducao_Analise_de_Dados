#%%
import numpy as np
# A partir de listas Python
v = np.array([1, 2, 3, 4, 5]) # 1-D
M = np.array([[1, 2, 3], [4, 5, 6]]) # 2-D (matriz)
# Arrays especiais
zeros = np.zeros((3, 4)) # zeros 3×4
uns = np.ones((2, 3)) # uns 2×3
ident = np.eye(3) # identidade 3×3
range_ = np.arange(0, 101, 10) # [0 2 4 6 8]
linsp = np.linspace(0, 1, 5) # [0.00 0.25 0.50 0.75 1.00]
aleats = np.random.rand(3, 3) # 3×3 com valores aleatórios em [0, 1)


print(aleats)


#%%
A = np.array([[10, 20, 30],
 [40, 50, 60],
 [70, 80, 90]])
# Elemento individual
print(A[0, 0]) # 10
print(A[2, 0]) # 80
# Linha / coluna completa
print(A[1, :]) # [40 50 60]
print(A[:, 2]) # [30 60 90]
# Sub-matriz
print(A[:2, 1:]) # [[20 30] [50 60]]
# Indexação booleana
B = A[A < 30]
print(B) # [60 70 80 90]
A[A < 30] = 0 # zera elementos menores que 30
