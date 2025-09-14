import tkinter as tk
from tkinter import filedialog
import cv2
import numpy as np
from PIL import Image, ImageTk

class AplicacaoFiltros:
    def __init__(self, root):
        self.root = root
        self.root.title("Remoção de Ruídos - Filtros com Preservação de Detalhes")

        # Para exibir a imagem
        self.label = tk.Label(self.root)
        self.label.grid(row=0, column=0, columnspan=4)

        # Botões de funcionalidades
        btn_carregar = tk.Button(self.root, text="Carregar Imagem", command=self.carregar_imagem)
        btn_carregar.grid(row=1, column=0)

        btn_resetar = tk.Button(self.root, text="Resetar Imagem", command=self.resetar_imagem)
        btn_resetar.grid(row=1, column=1)

        # Botões de filtros
        btn_filtro_media = tk.Button(self.root, text="Filtro Média", command=self.aplicar_filtro_media)
        btn_filtro_media.grid(row=2, column=0)

        btn_filtro_mediana = tk.Button(self.root, text="Filtro Mediana", command=self.aplicar_filtro_mediana)
        btn_filtro_mediana.grid(row=2, column=1)

        btn_filtro_gaussiano = tk.Button(self.root, text="Filtro Gaussiano", command=self.aplicar_filtro_gaussiano)
        btn_filtro_gaussiano.grid(row=2, column=2)

        # Variáveis para armazenar as imagens
        self.img_pil = None  # Armazena a imagem em formato PIL
        self.img_display = None  # Imagem para exibição
        self.img_original = None  # Armazena a imagem original

    # Funções de filtro para remoção de ruídos
    def aplicar_filtro_media(self):
        # Filtro de média 3x3 (suaviza levemente a imagem)
        if self.img_pil is not None:
            img_cv = np.array(self.img_pil)  # Converte PIL para array
            img_cv = cv2.cvtColor(img_cv, cv2.COLOR_RGB2BGR)  # Converte RGB para BGR (OpenCV usa BGR)
            img_filtrada = cv2.blur(img_cv, (3, 3))  # Aplica filtro de média
            self.img_pil = Image.fromarray(cv2.cvtColor(img_filtrada, cv2.COLOR_BGR2RGB))  # Converte de volta para PIL
            self.atualizar_imagem()

    def aplicar_filtro_mediana(self):
        # Filtro mediano 5x5 (ideal para ruídos sal e pimenta).
        if self.img_pil is not None:
            img_cv = np.array(self.img_pil)
            img_cv = cv2.cvtColor(img_cv, cv2.COLOR_RGB2BGR)
            img_filtrada = cv2.medianBlur(img_cv, 5)  # Aplica filtro mediano
            self.img_pil = Image.fromarray(cv2.cvtColor(img_filtrada, cv2.COLOR_BGR2RGB))
            self.atualizar_imagem()

    def aplicar_filtro_gaussiano(self):
        # Filtro Gaussiano com sigma = 0.5 (suaviza sem perder muitos detalhes).
        if self.img_pil is not None:
            img_cv = np.array(self.img_pil)
            img_cv = cv2.cvtColor(img_cv, cv2.COLOR_RGB2BGR)
            img_filtrada = cv2.GaussianBlur(img_cv, (5, 5), 0.5)  # Aplica filtro Gaussiano com sigma baixo
            self.img_pil = Image.fromarray(cv2.cvtColor(img_filtrada, cv2.COLOR_BGR2RGB))
            self.atualizar_imagem()

    # Função para carregar a imagem
    def carregar_imagem(self):      
        caminho_imagem = filedialog.askopenfilename() #Carrega a imagem selecionada pelo usuário.
        if caminho_imagem:
            self.img_pil = Image.open(caminho_imagem).convert("RGB")  # Abre a imagem como RGB
            self.img_original = self.img_pil.copy()  # Salva a original
            self.atualizar_imagem()

    # Atualizar imagem exibida
    def atualizar_imagem(self):
        # Atualiza a imagem exibida.
        self.img_display = ImageTk.PhotoImage(self.img_pil)  # Converte PIL para formato do Tkinter
        self.label.config(image=self.img_display)  # Exibe
        self.label.image = self.img_display  # Mantém referência

    # Função para resetar para a imagem original
    def resetar_imagem(self):
        # Reseta a imagem para o estado original.
        if self.img_original is not None:
            self.img_pil = self.img_original.copy()  # Restaura a imagem original
            self.atualizar_imagem()

# Inicializando a interface gráfica
if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacaoFiltros(root)
    root.mainloop()