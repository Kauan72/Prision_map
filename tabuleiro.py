import tkinter as tk
import os
import numpy as np
from tooltip import Tooltip
from matriz import criar_matriz

class Tabuleiro:
    def __init__(self, root):
        self.root = root
        self.matriz = criar_matriz()
        self.cores = ["white", "gray", "green", "blue",
                      "saddle brown", "black", "orange", "purple", "pink", "cyan"]
        self.cor_atual = 1
        self.tamanho_quadrado = 20
        self.largura_canvas = 42 * self.tamanho_quadrado
        self.altura_canvas = 42 * self.tamanho_quadrado
        self.create_widgets()

    def create_widgets(self):
        self.canvas = tk.Canvas(
            self.root, width=self.largura_canvas, height=self.altura_canvas)
        self.canvas.pack(side=tk.LEFT, padx=10, pady=10)

        self.quadrados = {}
        self.desenhar_quadrados()

        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)

        # Frame para os botões de cor
        self.frame_botoes = tk.Frame(self.root)
        self.frame_botoes.pack(side=tk.LEFT, padx=10, pady=10)

        cores = ["white", "gray", "green", "blue", "saddle brown", "black", "orange", "purple", "pink", "cyan"]
        textos = ["Branco", "Cinza", "Verde", "Azul", "Brown", "Rick", "Carl", "Daryl", "Glen", "Maggie"]
        
        for cor, texto in zip(cores, textos):
            botao = tk.Button(self.frame_botoes, text=texto, command=lambda cor=cor: self.mudar_cor(cor))
            botao.pack(side=tk.TOP, fill=tk.X)
            Tooltip(botao, f"cor {texto.lower()}")

        self.botao_salvar = tk.Button(
            self.root, text="Salvar Matriz", command=self.salvar_matriz)
        self.botao_salvar.pack(side=tk.LEFT, padx=10, pady=10)
        Tooltip(self.botao_salvar, "Salva a matriz atual")

        self.botao_carregar = tk.Button(
            self.root, text="Carregar Matriz", command=self.carregar_matriz)
        self.botao_carregar.pack(side=tk.LEFT, padx=10, pady=10)
        Tooltip(self.botao_carregar, "Carrega a matriz salva")

        self.botao_carregar_matriz_padrao = tk.Button(
            self.root, text="Mapa padrão", command=self.carregar_matriz_padrao)
        self.botao_carregar_matriz_padrao.pack(side=tk.LEFT, padx=10, pady=10)
        Tooltip(self.botao_carregar_matriz_padrao, "Carrega a matriz padrão")

        # Criar a legenda
        self.criar_legenda()

    def criar_legenda(self):
        legenda_frame = tk.Frame(self.root)
        legenda_frame.pack(side=tk.LEFT, padx=10, pady=10, anchor="nw")

        legenda_titulo = tk.Label(
            legenda_frame, text="Legenda", font=("Arial", 14, "bold"))
        legenda_titulo.pack(side=tk.TOP, anchor="w")

        legenda_itens = [
            ("Cinza escuro", "Asfalto", "gray"),
            ("Verde", "Grama", "green"),
            ("Marrom", "Terra", "saddle brown"),
            ("Cinza claro", "Paralelepípedo", "lightgray"),
            ("Azul", "Edifícios", "blue")
        ]

        for cor_nome, descricao, cor in legenda_itens:
            item_frame = tk.Frame(legenda_frame)
            item_frame.pack(side=tk.TOP, anchor="w")

            cor_label = tk.Label(
                item_frame, width=2, height=1, background=cor, relief="solid", borderwidth=1)
            cor_label.pack(side=tk.LEFT, padx=5)

            texto_label = tk.Label(item_frame, text=f"{descricao} ({cor_nome})", anchor="w")
            texto_label.pack(side=tk.LEFT)

    def desenhar_quadrados(self):
        self.quadrados = {}
        for i in range(42):
            for j in range(42):
                x1, y1 = j * self.tamanho_quadrado, i * self.tamanho_quadrado
                x2, y2 = x1 + self.tamanho_quadrado, y1 + self.tamanho_quadrado
                rect = self.canvas.create_rectangle(
                    x1, y1, x2, y2, fill=self.cores[self.matriz[i, j]])
                self.quadrados[(i, j)] = rect

    def on_click(self, event):
        self.colorir_quadrado(event.x, event.y)

    def on_drag(self, event):
        self.colorir_quadrado(event.x, event.y)

    def colorir_quadrado(self, x, y):
        j, i = x // self.tamanho_quadrado, y // self.tamanho_quadrado
        if 0 <= j < 42 and 0 <= i < 42:
            self.matriz[i, j] = self.cor_atual
            self.canvas.itemconfig(
                self.quadrados[(i, j)], fill=self.cores[self.cor_atual])

    def mudar_cor(self, nova_cor):
        if nova_cor in self.cores:
            self.cor_atual = self.cores.index(nova_cor)

    def salvar_matriz(self):
        pasta = "mapa"
        if not os.path.exists(pasta):
            os.makedirs(pasta)
        arquivo = os.path.join(pasta, "matriz.npy")
        np.save(arquivo, self.matriz)
        print(f"Matriz salva em {arquivo}")

    def carregar_matriz(self):
        arquivo = os.path.join("mapa", "matriz.npy")
        if os.path.exists(arquivo):
            self.matriz = np.load(arquivo)
            self.desenhar_quadrados()
            print(f"Matriz carregada de {arquivo}")
        else:
            print(f"Arquivo não encontrado: {arquivo}")

    def carregar_matriz_padrao(self):
        arquivo = os.path.join("mapa", "matrizPadrao.npy")
        if os.path.exists(arquivo):
            self.matriz = np.load(arquivo)
            self.desenhar_quadrados()
            print(f"Matriz carregada de {arquivo}")
        else:
            print(f"Arquivo não encontrado: {arquivo}")
