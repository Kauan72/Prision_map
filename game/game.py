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
CORES_PERSONAGENS = [(0, 255, 0), (255, 0, 0), (75, 0, 130), (255, 255, 0)]

# Criação da tela
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Fuga da prisão")

# Inicialização da fonte para o score
fonte_score = pygame.font.Font(None, 36)

# Variável para armazenar o score
score = 0

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

    return tabuleiro, matriz_traduzida

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
        pygame.draw.circle(tela, cor_personagem[count], (posicao[1] * TAMANHO_QUADRADO + TAMANHO_QUADRADO // 2, posicao[0] * TAMANHO_QUADRADO + TAMANHO_QUADRADO // 2), TAMANHO_QUADRADO // 2)
        count += 1

    pygame.draw.circle(tela, (0, 0, 0), (rick[1] * TAMANHO_QUADRADO + TAMANHO_QUADRADO // 2, rick[0] * TAMANHO_QUADRADO + TAMANHO_QUADRADO // 2), TAMANHO_QUADRADO // 2)

def desenhar_botao_start(started):
    cor_botao = (0, 128, 0)  # Verde
    largura_botao = 100
    altura_botao = 40
    posicao_botao = (10, ALTURA_TELA - altura_botao - 10, largura_botao, altura_botao)  # (x, y, largura, altura)
    pygame.draw.rect(tela, cor_botao, posicao_botao)
    fonte = pygame.font.Font(None, 36)
    texto = fonte.render('Start', True, (255, 255, 255))  # Texto branco
    texto_rect = texto.get_rect(center=(posicao_botao[0] + largura_botao // 2, posicao_botao[1] + altura_botao // 2))
    tela.blit(texto, texto_rect)

def exibir_score(score):
    """Desenha o score no topo esquerdo da tela."""
    texto_score = fonte_score.render(f'Score: {score}', True, (255, 255, 255))  # Texto branco
    tela.blit(texto_score, (10, 10))

def verifica_validade_cordenada(coordenada):
    x = coordenada[0]
    y = coordenada[1]
    if (x>=0 and x<=41) and (y>=0 and y<=41):
        return True
    return False

def devolver_cordenadas_adjacentes(posicao_atual):
    adjacentes = []

    x = posicao_atual[0]
    y = posicao_atual[1]
    #cima
    posicao_atual_aux = [x-1, y]
    if verifica_validade_cordenada(posicao_atual_aux):
        adjacentes.append(posicao_atual_aux)

    #baixo
    posicao_atual_aux = [x+1, y]
    if verifica_validade_cordenada(posicao_atual_aux):
        adjacentes.append(posicao_atual_aux)

    #esquerda
    posicao_atual_aux = [x, y-1]
    if verifica_validade_cordenada(posicao_atual_aux):
        adjacentes.append(posicao_atual_aux)

    #direita
    posicao_atual_aux = [x, y+1]
    if verifica_validade_cordenada(posicao_atual_aux):
        adjacentes.append(posicao_atual_aux)

    return adjacentes

def tradutor_custo_terreno(coordenadas, matriz_traduzida):
    x = coordenadas[0]
    y = coordenadas[1]

    tipo_terreno = matriz_traduzida[x][y]

    if tipo_terreno == "paralelepipedo":
        return 10
    elif tipo_terreno == "asfalto":
        return 1
    elif tipo_terreno == "grama":
        return 5
    elif tipo_terreno == "edificios":
        return -1
    elif tipo_terreno == "terra":
        return 3

def busca_a_estrela(rick, destino, matriz_traduzida):
    arvore = []
    nos_encontrados = []

    posicao_inicial = [0, 0, 0, 1000, 1000, rick, 1]#x, y, custo_de_chegada, heuristica, custo_total, nó_pai, flag_de_expansão
    posicao_inicial[0:2] = rick
    
    nos_encontrados.append(posicao_inicial)
    arvore.append(posicao_inicial)
    proximo_expandido = posicao_inicial
    
    caminho_encontrado = False
    caminho = []

    while True:

        #verificar se o proximo expandido é o final
        if proximo_expandido[0:2] == destino:
            caminho_encontrado = True

        while caminho_encontrado:
            posicao_atual = proximo_expandido[0:2]
            no_pai = proximo_expandido[5]

            while True:
                caminho.append(no_pai)

                if posicao_atual==rick:
                    caminho[-1] = rick
                    return caminho

                for no in arvore:
                    if no[0:2] == no_pai:
                        posicao_atual = no[0:2]
                        no_pai = no[5]  
                        
                         

                
            
        #Adquire as coordenadas dos nós adjascentes
        coordenadas_proximo_espandido = proximo_expandido[0:2]
        coordenadas_adjacentes = devolver_cordenadas_adjacentes(coordenadas_proximo_espandido)

        #preenche os dados dos nós adjascentes
        for coordenada in coordenadas_adjacentes:
            #Coordenadas
            coordenada_auxiliar = [0, 0, 0, 0, 0, [], 0]
            coordenada_auxiliar[0:2] = coordenada
            
            
            custo_terreno = tradutor_custo_terreno(coordenada, matriz_traduzida)

            if coordenada not in nos_encontrados:
                nos_encontrados.append(coordenada)
                if custo_terreno != -1:
                    #Custo de chegada
                    coordenada_auxiliar[2] = custo_terreno + proximo_expandido[2]

                    #Heuristica
                    x = coordenada[0]
                    y = coordenada[1]

                    x_destino = destino[0]
                    y_destino = destino[1]

                    x_aux = abs(x - x_destino)
                    y_aux = abs(y - y_destino)

                    distancia_manhattan = x_aux + y_aux

                    coordenada_auxiliar[3] = distancia_manhattan

                    #custo total
                    coordenada_auxiliar[4] = coordenada_auxiliar[2] + coordenada_auxiliar[3]

                    #Nó pai
                    coordenada_auxiliar[5] = coordenadas_proximo_espandido

                    #Flag de expansão
                    coordenada_auxiliar[6] = 0

                    arvore.append(coordenada_auxiliar)

        proximo_expandido_indice = 0
        menor = 9999999
        for i, no in enumerate(arvore):
            if no[6] == 0:
                if no[4] < menor:
                    menor = no[4]
                    proximo_expandido = no
                    proximo_expandido_indice = i

        arvore[proximo_expandido_indice][6] = 1

def main():
    tabuleiro, matriz_traduzida = criar_tabuleiro()
    clock = pygame.time.Clock()
    global score

    posicoes = [[13, 31], [5, 32], [35, 35], [32, 8]]
    saida = [39, 20]

    started = False
    tempo_mover_rick = 0
    intervalo_mover_rick = 500  # Milissegundos

    rick = [20, 12]
    caminho1 = busca_a_estrela(rick, posicoes[0], matriz_traduzida)
    caminho1 = caminho1[::-1]

    rick = [13, 31]
    caminho2 = busca_a_estrela(rick, posicoes[1], matriz_traduzida)
    caminho2 = caminho2[::-1]

    rick = [5, 32]
    caminho3 = busca_a_estrela(rick, posicoes[2], matriz_traduzida)
    caminho3 = caminho3[::-1]

    rick = [35, 35]
    caminho4 = busca_a_estrela(rick, posicoes[3], matriz_traduzida)
    caminho4 = caminho4[::-1]

    rick = [32, 8]
    caminho5 = busca_a_estrela(rick, saida, matriz_traduzida)
    caminho5 = caminho5[::-1]

    caminho = caminho1 + caminho2 + caminho3 + caminho4 + caminho5
    caminho.pop(0)

    rick = [20, 12]

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
                if len(caminho) > 0:
                    print(caminho)
                    proxima_posicao = caminho.pop(0)
                    rick = proxima_posicao
                if rick == posicoes[0]:
                    posicoes.pop(0)
                    CORES_PERSONAGENS.pop(0)

                terreno_custo = tradutor_custo_terreno(proxima_posicao, matriz_traduzida)
                score+=terreno_custo

                tempo_mover_rick = agora

        # Desenhar o tabuleiro e personagens
        desenhar_tabuleiro(tabuleiro)
        adicionar_personagens(rick, posicoes)
        
        # Desenhar o botão "Start"
        desenhar_botao_start(started)

        #Exibe o score
        exibir_score(score)

        # Atualizar a tela
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
