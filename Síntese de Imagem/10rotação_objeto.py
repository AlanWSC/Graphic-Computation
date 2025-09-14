import tkinter as tk
import math
from tkinter import simpledialog, messagebox

class DesenhaRetangulo:
    def __init__(self, master):
        self.master = master
        self.canvas = tk.Canvas(self.master, width=700, height=700)
        self.canvas.pack()
        self.canvas.bind('<Button-1>', self.desenha_ponto)
        self.pontos = []
        self.angulo_rotacao = 0
        self.desenha_grid()

    def desenha_ponto(self, event):
        x = event.x
        y = event.y
        self.pontos.append((x, y))
        self.canvas.create_oval(x-3, y-3, x+3, y+3, fill='black')

        if len(self.pontos) == 3:
            self.desenha_triangulo()
            self.canvas.unbind('<Button-1>')  # Desabilita o evento de clique
            self.rotacionar_se_necessario()

    def desenha_triangulo(self):
        self.canvas.create_polygon(self.pontos, outline='black', fill='')

    def desenha_grid(self):
        # Desenha as linhas verticais do grid
        for x in range(0, 701, 20):
            self.canvas.create_line(x, 0, x, 700, fill='lightgray')

        # Desenha as linhas horizontais do grid
        for y in range(0, 701, 20):
            self.canvas.create_line(0, y, 700, y, fill='lightgray')

    def rotacionar_se_necessario(self):
        angulo = simpledialog.askfloat('Ângulo de Rotação', 'Insira o ângulo de rotação (em graus):')
        if angulo is not None:
            self.angulo_rotacao += angulo
            self.rotacao_triangulo()
            self.pergunta_outra_rotacao()

    def rotacao_triangulo(self):
        ponto_rotacao = self.pontos[-1]
        transla_ponto = [(x - ponto_rotacao[0], y - ponto_rotacao[1]) for x, y in self.pontos]
        ponto_rotacionado = []

        angulo = math.radians(self.angulo_rotacao)
        for x, y in transla_ponto:
            novo_x = x * math.cos(angulo) - y * math.sin(angulo)
            novo_y = x * math.sin(angulo) + y * math.cos(angulo)
            ponto_rotacionado.append((novo_x, novo_y))

        final_pontos = [(x + ponto_rotacao[0], y + ponto_rotacao[1]) for x, y in ponto_rotacionado]

        self.canvas.create_polygon(final_pontos, outline='black', fill='')

    def pergunta_outra_rotacao(self):
        resposta = messagebox.askyesno('Outra Rotação', 'Deseja inserir outra rotação?')
        if resposta:
            self.rotacionar_se_necessario()

janela = tk.Tk()
DesenhaRetangulo(janela)
janela.title('Rotacionando desenho em ângulo')
janela.mainloop()