import tkinter as tk
from tkinter import filedialog
import cv2
import numpy as np
from PIL import Image, ImageTk

class DetectaBordas:
    def __init__(self, root):
        self.root = root
        self.root.title("Detecção de Bordas")

        # Exibe a imagem
        self.label = tk.Label(self.root)
        self.label.grid(row=0, column=0, columnspan=4)

        # Botões para carregar e resetar a imagem
        btn_carregar = tk.Button(self.root, text="Carregar Imagem", command=self.carregar_imagem)
        btn_carregar.grid(row=1, column=0)

        btn_resetar = tk.Button(self.root, text="Resetar Imagem", command=self.resetar_imagem)
        btn_resetar.grid(row=1, column=1)

        # Botões para aplicar filtros
        btn_filtro_sobel = tk.Button(self.root, text="Filtro Sobel", command=self.aplicar_filtro_sobel)
        btn_filtro_sobel.grid(row=2, column=0)

        btn_filtro_prewitt = tk.Button(self.root, text="Filtro Prewitt", command=self.aplicar_filtro_prewitt)
        btn_filtro_prewitt.grid(row=2, column=1)

        btn_filtro_canny = tk.Button(self.root, text="Filtro Canny", command=self.aplicar_filtro_canny)
        btn_filtro_canny.grid(row=2, column=2)

        # Variáveis para armazenar imagens
        self.img_pil = None  # Imagem em formato PIL para exibição
        self.img_display = None  # Imagem convertida para o formato do Tkinter
        self.img_original = None  # Imagem original para reset
        self.img_cv = None  # Imagem em formato OpenCV para processamento

    # Função para aplicar filtro Sobel
    def aplicar_filtro_sobel(self):
        if self.img_cv is not None:
            sobelx = cv2.Sobel(self.img_cv, cv2.CV_64F, 1, 0, ksize=3)  # Filtro Sobel na direção x
            sobely = cv2.Sobel(self.img_cv, cv2.CV_64F, 0, 1, ksize=3)  # Filtro Sobel na direção y
            sobel_combined = cv2.magnitude(sobelx, sobely)  # Combina os resultados
            self.img_pil = Image.fromarray(np.uint8(sobel_combined))  # Converte para formato PIL
            self.atualizar_imagem()  # Atualiza a exibição

    # Função para aplicar filtro Prewitt
    def aplicar_filtro_prewitt(self):
        if self.img_cv is not None:
            # Define kernels de Prewitt
            kernelx = np.array([[1, 0, -1], [1, 0, -1], [1, 0, -1]], dtype=np.float32)
            kernely = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]], dtype=np.float32)
            
            # Aplica filtros de Prewitt
            prewittx = cv2.filter2D(self.img_cv, cv2.CV_64F, kernelx)
            prewitty = cv2.filter2D(self.img_cv, cv2.CV_64F, kernely)

            # Combina os resultados
            prewitt_combined = cv2.magnitude(prewittx, prewitty)
            prewitt_combined = np.clip(prewitt_combined, 0, 255).astype(np.uint8)  # Clipping e conversão
            self.img_pil = Image.fromarray(prewitt_combined)  # Converte para formato PIL
            self.atualizar_imagem()  # Atualiza a exibição

    # Função para aplicar filtro Canny
    def aplicar_filtro_canny(self):
        if self.img_cv is not None:
            edges = cv2.Canny(self.img_cv, 100, 200)  # Aplica filtro Canny
            self.img_pil = Image.fromarray(edges)  # Converte para formato PIL
            self.atualizar_imagem()  # Atualiza a exibição

    # Função para carregar imagem
    def carregar_imagem(self):
        caminho_imagem = filedialog.askopenfilename()  # Abre o seletor de arquivos
        if caminho_imagem:
            self.img_pil = Image.open(caminho_imagem).convert("RGB")  # Carrega a imagem em formato RGB
            self.img_original = self.img_pil.copy()  # Salva a imagem original
            self.img_cv = cv2.imread(caminho_imagem, cv2.IMREAD_GRAYSCALE)  # Carrega a imagem em OpenCV
            self.atualizar_imagem()  # Atualiza a exibição

    # Função para atualizar a imagem exibida
    def atualizar_imagem(self):
        self.img_display = ImageTk.PhotoImage(self.img_pil)  # Converte a imagem PIL para PhotoImage
        self.label.config(image=self.img_display)  # Atualiza com a nova imagem
        self.label.image = self.img_display  # Mantém referência

    # Função para resetar para a imagem original
    def resetar_imagem(self):
        if self.img_original is not None:
            
            self.img_pil = self.img_original.copy()  # Restaura a imagem original
            self.img_cv = cv2.cvtColor(np.array(self.img_pil), cv2.COLOR_RGB2GRAY)  # Converte para escala de cinza
            self.atualizar_imagem()  # Atualiza a exibição

# Inicializando a interface gráfica
if __name__ == "__main__":
    root = tk.Tk()
    app = DetectaBordas(root)
    root.mainloop()
