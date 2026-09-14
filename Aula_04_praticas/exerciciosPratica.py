#%%

import numpy as np 

lista_notas = [7,10,5,3,8,2,6]

notas = np.array([7,10,5,3,8,2,6])
bonus = []
for n in lista_notas:
    bonus.append(n * 1.05)

bonus
# NumPy: o laço está dentro da biblioteca, compilado
bonus = notas * 1.05

#%%
#print(bonus)
print(bonus[bonus>=6])
(bonus >= 6).mean()

#%%
#Exemplo Pandas 
import pandas as pd

s = pd.Series([72.5, 68.0, 91.3],
              index=["20261000", "20261001", "20261002"],
              name="nota_final")



#%%
s.values   # array([72.5, 68. , 91.3])  -> o ndarray NumPy por baixo
s.index    # Index(['20261000', '20261001', '20261002'], dtype='object')
s.dtype    # dtype('float64')

#%%
a = pd.Series([10, 20, 30], index=["x", "y", "z"])
b = pd.Series([ 1,  2,  3], index=["z", "y", "x"])   # ordem invertida

a + b
# x    13    <- 10 + 3, casado pelo rótulo "x"
# y    22
# z    31

#%%
#Exemplos DataFrame
df = pd.DataFrame({"campus": ["Natal-Central", "Mossoró"],
                   "alunos": [98, 70]})

#%%
#verificar quantidade de linhas e colunas
df.shape

#%%
# verificar nome das colunas
df.columns

#%%
df.dtypes

#%%
df.to_numpy()

#%%
len(df)

#%%
df = pd.read_csv('../Aula_04_exercicios_iloc_loc/dados/matriculas_ifrn_2026.csv',sep=';')
df

#%%
df.info()

#%%
notas = df['nota_final']

#%%
df.loc[df["turno"] == "Noturno","nota_final"]

#%%
df.iloc[df["turno"] == "Noturno", 0:1]  