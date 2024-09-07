import pygame
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
CORES_PERSONAGENS = [(255, 0, 0), (0, 255, 0), (75, 0, 130), (255, 255, 0)]  # Vermelho, verde, azul e amarelo

# Criação da tela
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Tabuleiro com Terrenos e Personagens")

def carrega_matriz_traduzida(matriz_traduzida):
    matriz_traduzida = np.zeros((42, 42), dtype=object)
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
def adicionar_personagens(rick, posicoes):
    count = 0
    for posicao in posicoes:
        cor_personagem = CORES_PERSONAGENS
        pygame.draw.circle(tela, cor_personagem[count], (posicao[0] * TAMANHO_QUADRADO + TAMANHO_QUADRADO // 2, posicao[1] * TAMANHO_QUADRADO + TAMANHO_QUADRADO // 2), TAMANHO_QUADRADO // 2)
        count += 1

    pygame.draw.circle(tela, (0, 0, 0), (rick[0] * TAMANHO_QUADRADO + TAMANHO_QUADRADO // 2, rick[1] * TAMANHO_QUADRADO + TAMANHO_QUADRADO // 2), TAMANHO_QUADRADO // 2)

def mover_rick(rick):
    pass  # Esta função ainda não está implementada

def desenhar_botao(started):
    cor_botao = (0, 128, 0)  # Verde
    largura_botao = 100
    altura_botao = 40
    posicao_botao = (10, ALTURA_TELA - altura_botao - 10, largura_botao, altura_botao)  # (x, y, largura, altura)
    pygame.draw.rect(tela, cor_botao, posicao_botao)
    fonte = pygame.font.Font(None, 36)
    texto = fonte.render('Start', True, (255, 255, 255))  # Texto branco
    texto_rect = texto.get_rect(center=(posicao_botao[0] + largura_botao // 2, posicao_botao[1] + altura_botao // 2))
    tela.blit(texto, texto_rect)

def main():
    tabuleiro = criar_tabuleiro()
    clock = pygame.time.Clock()

    rick = [12, 20]
    posicoes = [[32, 5], [31, 13], [35, 35], [8, 32]]

    started = False
    tempo_mover_rick = 0
    intervalo_mover_rick = 500  # Milissegundos

    # Loop principal do jogo
    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if 10 < x < 10 + 100 and ALTURA_TELA - 40 - 10 < y < ALTURA_TELA - 10:
                    started = True

        # Atualiza a posição de Rick se o jogo tiver começado e o tempo permitir
        if started:
            agora = pygame.time.get_ticks()
            if agora - tempo_mover_rick >= intervalo_mover_rick:
                #Melhor Rota: ['Preto', 'Verde', 'Vermelho', 'Roxo', 'Amarelo', 'Sa�da']
                #Custo Total: 117
                rick[0] += 1
                tempo_mover_rick = agora

        # Desenhar o tabuleiro e personagens
        desenhar_tabuleiro(tabuleiro)
        adicionar_personagens(rick, posicoes)
        
        # Desenhar o botão "Start"
        desenhar_botao(started)

        # Atualizar a tela
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
