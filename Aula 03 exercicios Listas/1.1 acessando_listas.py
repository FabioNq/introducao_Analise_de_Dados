
#%%
frutas = ['maçã','banana','abacaxi']
frutas.append('abacate')

#%%
frutas.sort()
print(frutas)

#%%
frutas.reverse()
print()


#%%
# for simples
for fruta in frutas:
 print(fruta)
# enumerate — índice + valor
for i, fruta in enumerate(frutas):
 print(f"{i}: {fruta}")
# list comprehension — cria lista nova
quadrados = [x**2 for x in range(1, 6)]

print(quadrados)
# [1, 4, 9, 16, 25]
# com filtro
pares = [x for x in range(10) if x % 2 == 0]


#%%
catalogo = {
 "notebook": {"preco": 3200.00, "estoque": 15},
 "mouse": {"preco": 89.90, "estoque": 40},
 "teclado": {"preco": 150.00, "estoque": 8},
}
def exibir_catalogo(cat):
 print(f"{"Produto":<12} {"Preço":>10} {"Estoque":>9}")
 print("-" * 34)
 for produto, info in cat.items():
    print(f"{produto:<12} R${info["preco"]:>8.2f} {info["estoque"]:>9}")
exibir_catalogo(catalogo)
# Total em estoque

total = sum(i["preco"] * i["estoque"] for i in catalogo.values())
print(f"\nValor total em estoque: R$ {total:,.2f}")

#%% 

# Numpy

