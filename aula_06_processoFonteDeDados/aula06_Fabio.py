

#%%
import pandas as pd
import sqlite3
import json
import os
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt

#%%
print(os.getcwdb())

#%%
with open("dados/cnes_rn_amostra.json", "r", encoding="utf-8") as f:
    payload = json.load(f)

#%%
print(payload)

#%%
print(f" fonte      :{payload['fonte']}")
print(f" endpoint   :{payload['endpoint']}")
print(f" coletado em: {payload['data_coleta']}")
print(f" licença : {payload['licenca']}")
print(f" observação : {payload['observacao']}")

df = pd.DataFrame(payload["registros"])
print(f" \n {df.shape[0]} estabelecimentos, {df['municipio'].nunique()} municipio")
print(df.groupby("municipio").size().sort_values(ascending=False))


#%%
# Passando os dados para o banco de dados

con = sqlite3.connect("cnes.db")
df.to_sql("estabelecimentos",con,index=False,if_exists="replace")

consulta ='''
    SELECT  municipio,
            descricao_tipo_unidade,
            COUNT(*) as n
    FROM estabelecimentos
    WHERE descricao_tipo_unidade IN ('HOSPITAL GERAL', 'CENTRO DE SAUDE/UNIDADE BASICA')
    GROUP BY municipio,descricao_tipo_unidade
    ORDER BY n DESC
'''
resultado_sql = pd.read_sql(consulta,con)
print(resultado_sql.to_string(index=False))
con.close()



#%%
# CONVERTENDO OS DADOS EM CSV E PARQUET
df.to_csv("dados/cnes_rn_amostra.csv", index=False, sep=";", decimal=",", encoding="utf8")

df.to_parquet("dados/cnes_rn_amostra.parquet", index=False)


#%%
#convertendo XML
root = ET.Element("estabelecimentos")
for _, row in df.head(3).iterrows():
    el = ET.SubElement(root, "estabelecimento")
    for campo in ["municipio",  "descricao_tipo_unidade", "latitude", "longitude"]:
        sub = ET.SubElement(el, campo)
        sub.text = str(row[campo])
        ET.ElementTree(root).write("dados/ cnes_amostra_3linhas.xml",
encoding="utf-8", xml_declaration=True)
        
        
#%%
# Verificar Tamanho dos Dados
tamanho_csv = "dados/cnes_rn_amostra.csv"
tamanho_parquet = "dados/cnes_rn_amostra.parquet"
tamanho_xml = "dados/ cnes_amostra_3linhas.xml"

tamanho_bytes_csv = os.path.getsize(tamanho_csv)
tamanho_bytes_parquet = os.path.getsize(tamanho_parquet)
tamanho_bytes_xml = os.path.getsize(tamanho_xml)

print(f"CSV {tamanho_bytes_csv} bytes")
print(f"parquet {tamanho_bytes_parquet} bytes")
print(f"xml {tamanho_bytes_xml} bytes")



#%%
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

			
		

with open("dados/rn_contorno.json", encoding="utf-8") as f:
    contorno = json.load(f) # GeoJSON: lista de coordenadas [longitude, latitude]
xs = [c[0] for c in contorno["coordinates"]]
ys = [c[1] for c in contorno["coordinates"]]    
fig, ax = plt.subplots(figsize=(7, 6.5))
ax.plot(xs, ys, color="#00693e", linewidth=1.5)
ax.fill(xs, ys, color="#00693e", alpha=0.05)
for municipio, grupo in df.groupby("municipio"):
    ax.scatter(grupo["longitude"], grupo["latitude"], s=28, alpha=0.85,
    color=cores.get(municipio, "gray"),
label=f"{municipio} ({len(grupo)})")
plt.legend()    
fig.savefig("mapa_estabelecimentos_rn.png", dpi=150)