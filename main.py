import numpy as np
import tkinter as tk
import os

def criar_matriz():
    # Cria uma matriz 42x42 com valores 0 (representando a cor branca)
    return np.zeros((42, 42), dtype=int)

class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event):
        if self.tooltip:
            return
        x = self.widget.winfo_rootx() + self.widget.winfo_width()
        y = self.widget.winfo_rooty() + self.widget.winfo_height()
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        label = tk.Label(self.tooltip, text=self.text, background="lightyellow", relief="solid", borderwidth=1)
        label.pack()
    
    def hide_tooltip(self, event):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

class Tabuleiro:
    def __init__(self, root):
        self.root = root
        self.matriz = criar_matriz()
        #Na matriz os números são correspondentes a ordem das cores na variável self.cores. Ex: white=1, green=3, blue==4
        self.cores = ["white", "gray", "green", "blue", "saddle brown", "black", "orange", "purple", "pink", "cyan"]
        self.cor_atual = 1  # Índice da cor atual (inicialmente cinza)
        self.tamanho_quadrado = 20  # Novo tamanho dos quadrados
        self.largura_canvas = 42 * self.tamanho_quadrado
        self.altura_canvas = 42 * self.tamanho_quadrado
        self.create_widgets()
    
    def create_widgets(self):
        # Configuração do Canvas
        self.canvas = tk.Canvas(self.root, width=self.largura_canvas, height=self.altura_canvas)
        self.canvas.pack(side=tk.LEFT, padx=10, pady=10)
        
        self.quadrados = {}
        self.desenhar_quadrados()
        
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        
        # Frame para os botões de cor
        self.frame_botoes = tk.Frame(self.root)
        self.frame_botoes.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Botões de cor
        self.botao_branco = tk.Button(self.frame_botoes, text="Branco", command=lambda: self.mudar_cor("white"))
        self.botao_branco.pack(side=tk.TOP, fill=tk.X)
        
        self.botao_cinza = tk.Button(self.frame_botoes, text="Cinza", command=lambda: self.mudar_cor("gray"))
        self.botao_cinza.pack(side=tk.TOP, fill=tk.X)
        
        self.botao_verde = tk.Button(self.frame_botoes, text="Verde", command=lambda: self.mudar_cor("green"))
        self.botao_verde.pack(side=tk.TOP, fill=tk.X)
        
        self.botao_azul = tk.Button(self.frame_botoes, text="Azul", command=lambda: self.mudar_cor("blue"))
        self.botao_azul.pack(side=tk.TOP, fill=tk.X)

        self.botao_brown = tk.Button(self.frame_botoes, text="Brown", command=lambda: self.mudar_cor("saddle brown"))
        self.botao_brown.pack(side=tk.TOP, fill=tk.X)

        self.botao_black = tk.Button(self.frame_botoes, text="Rick", command=lambda: self.mudar_cor("black"))
        self.botao_black.pack(side=tk.TOP, fill=tk.X)
        Tooltip(self.botao_black, "cor preta")

        self.botao_orange = tk.Button(self.frame_botoes, text="Carl", command=lambda: self.mudar_cor("orange"))
        self.botao_orange.pack(side=tk.TOP, fill=tk.X)
        Tooltip(self.botao_orange, "cor laranja")

        self.botao_purple = tk.Button(self.frame_botoes, text="Daryl", command=lambda: self.mudar_cor("purple"))
        self.botao_purple.pack(side=tk.TOP, fill=tk.X)
        Tooltip(self.botao_purple, "cor roxa")

        self.botao_pink = tk.Button(self.frame_botoes, text="Glen", command=lambda: self.mudar_cor("pink"))
        self.botao_pink.pack(side=tk.TOP, fill=tk.X)
        Tooltip(self.botao_pink, "cor rosa")

        self.botao_cyan = tk.Button(self.frame_botoes, text="Maggie", command=lambda: self.mudar_cor("cyan"))
        self.botao_cyan.pack(side=tk.TOP, fill=tk.X)
        Tooltip(self.botao_cyan, "cor azul ciano")
        
        # Adicionando botões para salvar e carregar a matriz
        self.botao_salvar = tk.Button(self.root, text="Salvar Matriz", command=self.salvar_matriz)
        self.botao_salvar.pack(side=tk.LEFT, padx=10, pady=10)
        Tooltip(self.botao_salvar, "Salva a matriz atual")
        
        self.botao_carregar = tk.Button(self.root, text="Carregar Matriz", command=self.carregar_matriz)
        self.botao_carregar.pack(side=tk.LEFT, padx=10, pady=10)
        Tooltip(self.botao_carregar, "Carrega a matriz salva")
        
        self.botao_carregar_matriz_padrao = tk.Button(self.root, text="Mapa padrão", command=self.carregar_matriz_padrao)
        self.botao_carregar_matriz_padrao.pack(side=tk.LEFT, padx=10, pady=10)
        Tooltip(self.botao_carregar_matriz_padrao, "Carrega a matriz padrão")
    
    def desenhar_quadrados(self):
        self.quadrados = {}
        for i in range(42):
            for j in range(42):
                x1, y1 = j * self.tamanho_quadrado, i * self.tamanho_quadrado  # Novo cálculo para coordenadas
                x2, y2 = x1 + self.tamanho_quadrado, y1 + self.tamanho_quadrado
                rect = self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.cores[self.matriz[i, j]])
                self.quadrados[(i, j)] = rect

    def on_click(self, event):
        self.colorir_quadrado(event.x, event.y)
    
    def on_drag(self, event):
        self.colorir_quadrado(event.x, event.y)
    
    def colorir_quadrado(self, x, y):
        j, i = x // self.tamanho_quadrado, y // self.tamanho_quadrado  # Novo cálculo para coordenadas
        if 0 <= j < 42 and 0 <= i < 42:
            self.matriz[i, j] = self.cor_atual
            self.canvas.itemconfig(self.quadrados[(i, j)], fill=self.cores[self.cor_atual])

    def mudar_cor(self, nova_cor):
        if nova_cor in self.cores:
            self.cor_atual = self.cores.index(nova_cor)

    def salvar_matriz(self):
        # Define o caminho fixo para salvar o arquivo
        pasta = "mapa"
        if not os.path.exists(pasta):
            os.makedirs(pasta)  # Cria a pasta se não existir
        arquivo = os.path.join(pasta, "matriz.npy")
        np.save(arquivo, self.matriz)
        print(f"Matriz salva em {arquivo}")

    def carregar_matriz(self):
        # Define o caminho fixo para carregar o arquivo
        arquivo = os.path.join("mapa", "matriz.npy")
        if os.path.exists(arquivo):
            self.matriz = np.load(arquivo)
            self.desenhar_quadrados()
            print(f"Matriz carregada de {arquivo}")
        else:
            print(f"Arquivo não encontrado: {arquivo}")

    def carregar_matriz_padrao(self):
        # Define o caminho fixo para carregar o arquivo do mapa padrão
        arquivo = os.path.join("mapa", "matrizPadrao.npy")
        if os.path.exists(arquivo):
            self.matriz = np.load(arquivo)
            self.desenhar_quadrados()
            print(f"Matriz carregada de {arquivo}")
        else:
            print(f"Arquivo não encontrado: {arquivo}")



if __name__ == "__main__":
    root = tk.Tk()
    app = Tabuleiro(root)
    root.mainloop()
