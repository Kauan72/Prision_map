import pygame
import random
import numpy as np
import os

# Inicialização do Pygame
pygame.init()

# Dimensões do tabuleiro e dos quadrados
TAMANHO_QUADRADO = 20
NUM_QUADRADOS = 42
LARGURA_TELA = ALTURA_TELA = NUM_QUADRADOS * TAMANHO_QUADRADO

# Cores para diferentes tipos de terreno
CORES_TERRENO = {
    "paralelepipedo": (255, 255, 255),  # Branco
    "asfalto": (128, 128, 128),         # Cinza
    "grama": (0, 128, 0),               # Verde
    "edificios": (0, 0, 255),           # Azul
    "terra": (139, 69, 19)              # Saddle brown (marrom)
}

# Personagens representados por cores
CORES_PERSONAGENS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]  # Vermelho, verde, azul e amarelo

# Criação da tela
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Tabuleiro com Terrenos e Personagens")

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

# Função para criar o tabuleiro
def criar_tabuleiro():
    matriz_traduzida = np.zeros((42, 42), dtype=object)
    matriz_traduzida = carrega_matriz_traduzida(matriz_traduzida)

    tabuleiro = []
    tipos_terreno = list(CORES_TERRENO.keys())

    for linha in range(NUM_QUADRADOS):
        linha_tabuleiro = []
        for coluna in range(NUM_QUADRADOS):
            choice = matriz_traduzida[linha][coluna]

            tipo_terreno = choice
            linha_tabuleiro.append(tipo_terreno)
        tabuleiro.append(linha_tabuleiro)
    
    return tabuleiro

# Função para desenhar o tabuleiro
def desenhar_tabuleiro(tabuleiro):
    for linha in range(NUM_QUADRADOS):
        for coluna in range(NUM_QUADRADOS):
            tipo_terreno = tabuleiro[linha][coluna]
            cor = CORES_TERRENO[tipo_terreno]
            pygame.draw.rect(tela, cor, (coluna * TAMANHO_QUADRADO, linha * TAMANHO_QUADRADO, TAMANHO_QUADRADO, TAMANHO_QUADRADO))

# Função para adicionar personagens ao tabuleiro
def adicionar_personagens():
    posicoes = []
    while len(posicoes) < 4:
        x = random.randint(0, NUM_QUADRADOS - 1)
        y = random.randint(0, NUM_QUADRADOS - 1)
        if (x, y) not in posicoes:  # Certifica-se de que personagens não se sobreponham
            posicoes.append((x, y))
            cor_personagem = CORES_PERSONAGENS[len(posicoes) - 1]
            pygame.draw.circle(tela, cor_personagem, (x * TAMANHO_QUADRADO + TAMANHO_QUADRADO // 2, y * TAMANHO_QUADRADO + TAMANHO_QUADRADO // 2), TAMANHO_QUADRADO // 2)

# Função principal do jogo
def main():
    tabuleiro = criar_tabuleiro()
    clock = pygame.time.Clock()

    # Loop principal do jogo
    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        # Desenhar o tabuleiro e personagens
        desenhar_tabuleiro(tabuleiro)
        adicionar_personagens()

        # Atualizar a tela
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
