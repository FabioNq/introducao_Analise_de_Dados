
#%%
import pandas as pd
import numpy as np

#%%


df = pd.read_csv("dados/matriculas_ifrn_2026.csv", sep=";", decimal=",",
                 encoding="utf-8", dtype={"matricula": "string"})
df["campus"] = df["campus"].str.strip()
df = df.drop_duplicates().reset_index(drop=True)

campi  = pd.read_excel("dados/campi_ifrn.xlsx", sheet_name="campi")
cursos = pd.read_excel("dados/campi_ifrn.xlsx", sheet_name="cursos")

print(f"matrículas: {df.shape} | campi: {campi.shape} | cursos: {cursos.shape}")

#%%
campi

#%%
cursos
#%%
## calcula média das notas finais por Campus 

media_por_campus = df.groupby(["campus",'curso'])["nota_final"].mean().round(2)
media_por_campus.sort_values(ascending=False)
media_por_campus

#%%

#Contar tamanho por grupos 
tamanho = df.groupby('curso').size()
tamanho.sort_values(ascending=False)

#conta apenas os valores não ausentes daquela coluna especifica
contagem = df.groupby('campus')['nota_final'].count()
ausentes = tamanho - contagem

contagem.sort_values(ascending=False)
#ausentes
ausentes

#%%
df.groupby("campus")['nota_final'].agg(['mean','median','std','count'])


#%%
#nomeacao das proprias estruturas 
df.groupby("turno").agg(
    nota_media = ("nota_final","mean"),
    nota_desvio=("nota_final","std"),
    idade=("idade", "median"),
    taxa_aprovacao =("situacao", lambda s:(s == "Aprovado").mean() * 100),).round(2)


#%%
df.pivot_table(values='nota_final',index="campus", columns='turno',aggfunc=['mean','std']).reset_index()


#%%
#MARGINS 
df.pivot_table(values="matricula", index="campus", columns="situacao",
              aggfunc="count", fill_value=0,
              margins=True, margins_name="Total")


#%%

# fill_value = preenche com 0 valores nulos ou vazios.
df.pivot_table(values="matricula", index="campus", columns="situacao",
              aggfunc="count", fill_value=0,
              margins=True, margins_name="Total")


#%%
# MERGE 
df_campi = df.merge(campi, on="campus", how="left", validate="m:1")
df_completo = df_campi.merge(cursos, on="curso", how="left", validate="m:1")
print(df_completo[["regiao","eixo_tecnologico"]].isna().sum())

