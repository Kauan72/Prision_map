import os
import numpy as np

def tradutor(terreno_numerico):
    if terreno_numerico==0:
        return "paralelepipedo"
    elif terreno_numerico==1:
        return "asfalto"
    elif terreno_numerico==2:
        return "grama"
    elif terreno_numerico==3:
        return "edificios"
    elif terreno_numerico==4:
        return "terra"

def converte_matriz(matriz, matriz_traduzida):

    for i in range(42):
        for j in range(42):
            matriz_traduzida[i][j] = tradutor(matriz[i][j])

def cria_matrizes():
    # Cria uma matriz 42x42 com valores 0 (representando a cor branca)
    matriz = np.zeros((42, 42), dtype=int)
    matriz_traduzida = np.zeros((42, 42), dtype=object)
    return matriz, matriz_traduzida

def carrega_matriz_padrao(matriz):
    # Define o caminho fixo para carregar o arquivo do mapa padrão
    arquivo = os.path.join("mapa", "matrizPadrao.npy")
    if os.path.exists(arquivo):
        matriz = np.load(arquivo)
        print(f"Matriz carregada de {arquivo}")
    else:
        print(f"Arquivo não encontrado: {arquivo}")

    return matriz

def salvar_matriz_traduzida(matriz_traduzida):
    # Define o caminho fixo para salvar o arquivo
    pasta = "mapa"
    if not os.path.exists(pasta):
        os.makedirs(pasta)  # Cria a pasta se não existir
    arquivo = os.path.join(pasta, "matriz_traduzida.npy")
    np.save(arquivo, matriz_traduzida)
    print(f"Matriz salva em {arquivo}")

def carrega_matriz_traduzida(matriz_traduzida):
    matriz_traduzida = np.zeros((42, 42), dtype=object)
    # Define o caminho fixo para carregar o arquivo do mapa padrão
    arquivo = os.path.join("mapa", "matriz_traduzida.npy")
    if os.path.exists(arquivo):
        matriz_traduzida = np.load(arquivo, allow_pickle=True)
        print(f"Matriz carregada de {arquivo}")
    else:
        print(f"Arquivo não encontrado: {arquivo}")

    return matriz_traduzida

matriz, matriz_traduzida = cria_matrizes()
matriz = carrega_matriz_padrao(matriz)

converte_matriz(matriz, matriz_traduzida)

salvar_matriz_traduzida(matriz_traduzida)



