import time
import numpy as np

escolas = [
    {"nome": "Escola A", "tipo": "Estadual", "media": 512.3, "participantes": 180},
    {"nome": "Escola B", "tipo": "Federal", "media": 610.7, "participantes": 95},
    {"nome": "Escola C", "tipo": "Privada", "media": 645.1, "participantes": 60},
    {"nome": "Escola D", "tipo": "Municipal", "media": 470.5, "participantes": 40},
    {"nome": "Escola E", "tipo": "Estadual", "media": 498.9, "participantes": 220},
    {"nome": "Escola F", "tipo": "Privada", "media": 630.2, "participantes": 75},
    {"nome": "Escola G", "tipo": "Federal", "media": 598.4, "participantes": 110},
    {"nome": "Escola H", "tipo": "Estadual", "media": 505.6, "participantes": 150},
]


def media_geral(lista_escolas):
    total = 0
    for escola in lista_escolas:
        total += escola["media"]
    return total / len(lista_escolas)


def filtrar_por_tipo(lista_escolas, tipo):
    return [e for e in lista_escolas if e["tipo"] == tipo]


def escola_com_maior_media(lista_escolas):
    maior = lista_escolas[0]
    for escola in lista_escolas[1:]:
        if escola["media"] > maior["media"]:
            maior = escola
    return maior


def parte1_python_puro():
    print("=== Parte 1: Python puro (listas, dicionários, funções) ===")
    print(f"Média geral (Python puro): {media_geral(escolas):.1f}")
    estaduais = filtrar_por_tipo(escolas, "Estadual")
    print(f"Escolas estaduais: {[e['nome'] for e in estaduais]}")
    melhor = escola_com_maior_media(escolas)
    print(f"Escola com maior média: {melhor['nome']} ({melhor['media']})")


def parte2_numpy():
    print("\n=== Parte 2: NumPy (arrays e operações vetorizadas) ===")
    medias = np.array([e["media"] for e in escolas])
    participantes = np.array([e["participantes"] for e in escolas])
    nomes = np.array([e["nome"] for e in escolas])

    print(f"Array de médias: {medias}")
    print(f"Média geral (NumPy): {medias.mean():.1f}")
    print(f"Desvio padrão: {medias.std():.1f}")
    print(f"Maior média: {medias.max():.1f} | Menor média: {medias.min():.1f}")

    peso = participantes / participantes.sum()
    media_ponderada = (medias * peso).sum()
    print(f"Média ponderada pelo nº de participantes: {media_ponderada:.1f}")

    acima_da_media = medias > medias.mean()
    print(f"Escolas acima da média geral: {nomes[acima_da_media].tolist()}")


def parte3_desempenho():
    print("\n=== Parte 3: Por que usar NumPy? ===")
    grande = np.random.default_rng(42).normal(500, 80, 1_000_000)

    inicio = time.perf_counter()
    soma_loop = 0.0
    for valor in grande:
        soma_loop += valor
    tempo_loop = time.perf_counter() - inicio

    inicio = time.perf_counter()
    soma_vetorizada = grande.sum()
    tempo_vetorizado = time.perf_counter() - inicio

    print(f"Soma de 1.000.000 de valores via loop Python puro: {tempo_loop*1000:.1f} ms")
    print(f"Soma de 1.000.000 de valores via NumPy (vetorizada): {tempo_vetorizado*1000:.2f} ms")
    print(f"NumPy foi aproximadamente {tempo_loop/tempo_vetorizado:.0f}x mais rápido")


def main():
    parte1_python_puro()
    parte2_numpy()
    parte3_desempenho()


if __name__ == "__main__":
    main()