

#%%
import pandas as pd
import sqlite3
import json
import xml.etree.ElementTree as ET
from pathlib import Path
import matplotlib.pyplot as plt

#especifica o diretorio onde encontram-se os dados.
DADOS = Path("dados")
#%%
#carrega o arquivo Json 
print("Passo 1 - Carregando Snapshot")
with open( DADOS / "cnes_rn_amostra.json", "r", encoding="utf-8") as f:
    payload = json.load(f)

#%%
print(payload)

#%%

##QUESTAO 01: 

print(f" fonte      :{payload['fonte']}")
print(f" endpoint   :{payload['endpoint']}")
print(f" coletado em: {payload['data_coleta']}")
print(f" licença : {payload['licenca']}")
print(f" observação : {payload['observacao']}")

df = pd.DataFrame(payload["registros"])
print(f" \n {df.shape[0]} estabelecimentos, {df['municipio'].nunique()} municipio")
print(df.groupby("municipio").size().sort_values(ascending=False))

#%%
df.info()

#%%
#QUESTÃO 02 : 
# criando o banco de dados e realizando a consulta, é possivel criar um arquivo de banco de dados e criar consultas separadas 

con = sqlite3.connect("cnes.db")
df.to_sql("estabelecimentos",con,index=False,if_exists="replace")

consulta ='''
    SELECT  municipio,
            descricao_tipo_unidade,
            COUNT(*) as n
    FROM estabelecimentos
    WHERE descricao_tipo_unidade IN ('HOSPITAL GERAL', 'CENTRO DE SAUDE/UNIDADE BASICA','CONSULTORIO ISOLADO')
    GROUP BY municipio,descricao_tipo_unidade
    ORDER BY n DESC
'''
resultado_sql = pd.read_sql(consulta,con)
print(resultado_sql.to_string(index=False))
con.close()


#%%
# CONVERTENDO OS DADOS EM CSV E PARQUET
df.to_csv(DADOS / "cnes_rn_amostra.csv", index=False, sep=";", decimal=",", encoding="utf8")
df.to_parquet(DADOS /"cnes_rn_amostra.parquet",engine='fastparquet', index=False) 

#%%
#convertendo XML
root = ET.Element("estabelecimentos")
for _, row in df.head(3).iterrows():
    el = ET.SubElement(root, "estabelecimento")
    for campo in ["municipio",  "descricao_tipo_unidade", "latitude", "longitude"]:
        sub = ET.SubElement(el, campo)
        sub.text = str(row[campo])
        ET.ElementTree(root).write(DADOS/ "cnes_amostra_3linhas.xml",
encoding="utf-8", xml_declaration=True)
        
        
#%%
# QUESTAO 03 : Verificar Tamanho dos Dados em bytes
print(f"CSV : {Path(DADOS/'cnes_rn_amostra.csv').stat().st_size} bytes")
print(f"Parquet : {Path(DADOS/'cnes_rn_amostra.parquet').stat().st_size} bytes")
print(f"XML: {Path(DADOS/'cnes_amostra_3linhas.xml').stat().st_size} bytes")


#%%
# QUESTÃO 04 : 


 # verificar se o site possui o robots.txt e saber quais dados são acessiveis para realização do Scrapping,  verificação da Creative  Commons(CC) e suas siglas, By: exige atribuição, SA(share-alike) exige que derivados usem a mesma licença, NC proibe os dados para uso comercial, ND proibe modificações. os dados consumidos foram do CNES que são regidos pela Lei de Acesso a Informação(Lei 12.527/2011) e por políticas de dados abertos, uso livre,comercial e com boa prática de citar a fonte.




# QUESTÃO 05 Mapa. 
#CRIAÇÃO DO MAPA 
#criação de dicionario de dados para representar as cores dentro do mapa
cores = {
    'Natal':'blue',
    'Mossoro':'red',
    'Acu':'yellow',
    'Caico':'purple',
    'CearaMirim': 'pink',
    'CurraisNovos':'brown',
    'Parnamirim' : 'black',
    'PauDosFerro': 'cyan'
    }

			
		

#Abre o arquivo de contorno do mapa do RN
with open("dados/rn_contorno.json", encoding="utf-8") as f:
    contorno = json.load(f)
print(contorno)
#xs pega a coordenada do eixo x    
xs = [c[0] for c in contorno["coordinates"]]

#xs pega a coordenada do eixo y
ys = [c[1] for c in contorno["coordinates"]]    

#criação do grafico de contorno
fig, ax = plt.subplots(figsize=(7, 5))
ax.plot(xs, ys, color="#8D9731", linewidth=1.5)
ax.fill(xs, ys, color="#BDF7DA", alpha=0.05)
# realiza o desenho de cada municipio com ax.scatter de acordo com a latitude e longitude.
for municipio, grupo in df.groupby("municipio"):
    ax.scatter(grupo["longitude"], grupo["latitude"], s=100, alpha=0.85,
    color=cores.get(municipio, "gray"),
label=f"{municipio} ({len(grupo)})")
#exibe a legenda para não ficar na frente do mapa do RN
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)    
fig.savefig("mapa_estabelecimentos_rn.png", dpi=150)


