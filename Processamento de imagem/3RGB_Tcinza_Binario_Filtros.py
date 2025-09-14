import tkinter as tk
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk

class ProcessaImagem:
    def __init__(self, root):
        self.root = root
        self.root.title("RGB -> Tons de Cinza -> Binário e Filtros")

        self.img = None
        self.img_exibida = None

        # Criar um label para exibir a imagem
        self.label_imagem = tk.Label(root)
        self.label_imagem.pack()

        # Frame para Funções
        frame_funcoes = tk.Frame(root)
        frame_funcoes.pack(pady=10)

        self.botao_carregar = tk.Button(frame_funcoes, text="Carregar Imagem", command=self.carregar_imagem)
        self.botao_carregar.pack(side=tk.LEFT)

        # Frame para Tipos
        frame_tipos = tk.Frame(root)
        frame_tipos.pack(pady=10)

        self.botao_cinza = tk.Button(frame_tipos, text="Tons de Cinza", command=self.converter_para_cinza)
        self.botao_cinza.pack(side=tk.LEFT)

        self.botao_binaria = tk.Button(frame_tipos, text="Binária", command=self.converter_para_binario)
        self.botao_binaria.pack(side=tk.LEFT)

        self.botao_rgb = tk.Button(frame_tipos, text="RGB", command=self.converter_para_rgb)
        self.botao_rgb.pack(side=tk.LEFT)

        # Frame para Filtros
        frame_filtros = tk.Frame(root)
        frame_filtros.pack(pady=10)

        self.botao_media = tk.Button(frame_filtros, text="Filtro de Média", command=self.aplicar_filtro_media)
        self.botao_media.pack(side=tk.LEFT)

        self.botao_mediana = tk.Button(frame_filtros, text="Filtro Mediano", command=self.aplicar_filtro_mediana)
        self.botao_mediana.pack(side=tk.LEFT)

        self.botao_gaussiano = tk.Button(frame_filtros, text="Filtro Gaussiano", command=self.aplicar_filtro_gaussiano)
        self.botao_gaussiano.pack(side=tk.LEFT)

    # Função para carregar a imagem
    def carregar_imagem(self):
        caminho_arquivo = filedialog.askopenfilename(filetypes=[("Arquivos de Imagem", "*.jpg;*.jpeg;*.png;*.bmp;*.tiff")])
        if not caminho_arquivo:
            return

        self.img = cv2.imread(caminho_arquivo)
        self.img_exibida = self.img.copy()  # Cópia da imagem original para manipulação
        self.exibir_imagem(self.img_exibida)

    # Função para exibir a imagem
    def exibir_imagem(self, img_cv):
        img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)  # OpenCV usa BGR, então convertendo para RGB
        img_pil = Image.fromarray(img_rgb)
        img_tk = ImageTk.PhotoImage(img_pil)
        self.label_imagem.config(image=img_tk)
        self.label_imagem.image = img_tk  # Referência para evitar coleta de lixo

    # Função para converter para tons de cinza
    def converter_para_cinza(self):
        if self.img is not None:
            self.img_exibida = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
            self.exibir_imagem(cv2.cvtColor(self.img_exibida, cv2.COLOR_GRAY2BGR))

    # Função para converter para binário
    def converter_para_binario(self):
        if self.img is not None:
            img_cinza = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
            _, self.img_exibida = cv2.threshold(img_cinza, 128, 255, cv2.THRESH_BINARY)
            self.exibir_imagem(cv2.cvtColor(self.img_exibida, cv2.COLOR_GRAY2BGR))

    # Função para converter de volta para RGB
    def converter_para_rgb(self):
        if self.img is not None:
            self.img_exibida = self.img.copy()  # Garantir que estamos usando a imagem original
            self.exibir_imagem(self.img_exibida)

    # Função para aplicar filtro de média
    def aplicar_filtro_media(self):
        if self.img_exibida is not None:
            self.img_exibida = cv2.blur(self.img_exibida, (5, 5))
            self.exibir_imagem(self.img_exibida)

    # Função para aplicar filtro mediano
    def aplicar_filtro_mediana(self):
        if self.img_exibida is not None:
            self.img_exibida = cv2.medianBlur(self.img_exibida, 5)
            self.exibir_imagem(self.img_exibida)

    # Função para aplicar filtro gaussiano
    def aplicar_filtro_gaussiano(self):
        if self.img_exibida is not None:
            self.img_exibida = cv2.GaussianBlur(self.img_exibida, (5, 5), 0)
            self.exibir_imagem(self.img_exibida)

# Criar a janela principal
root = tk.Tk()
app = ProcessaImagem(root)

# Iniciar o loop principal
root.mainloop()
