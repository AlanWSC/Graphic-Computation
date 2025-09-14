import tkinter as tk
from tkinter import simpledialog, messagebox

class DesenhaRetangulo:
    def __init__(self, master):
        self.master = master
        self.canvas = tk.Canvas(self.master, width=400, height=400)
        self.canvas.pack()
        self.canvas.bind('<Button-1>', self.desenha_ponto)
        self.pontos = []
        self.ponto_fixo = None  # Ponto fixo definido pelo primeiro clique
        self.redesenha_borda()
        self.desenha_grid()  # Adiciona o grid

    def desenha_ponto(self, event):
        x = event.x
        y = event.y
        if not self.ponto_fixo:
            # Define o primeiro clique como ponto fixo
            self.ponto_fixo = (x, y)
            self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill='black')
        else:
            self.pontos.append((x, y))
            self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill='black')

        if len(self.pontos) == 2:
            self.desenha_triangulo()
            self.aplica_transformacao()
            self.canvas.unbind('<Button-1>')  # Desabilita o evento de clique
            self.pergunta_transformacao()

    def desenha_triangulo(self):
        self.canvas.create_polygon(
            [self.ponto_fixo] + self.pontos, outline='black', fill='')

    def aplica_transformacao(self):
        ponto_x = self.ponto_fixo[0]
        ponto_y = self.ponto_fixo[1]
        
        fator_x = simpledialog.askfloat('Fator de Escala', 'Digite o fator de escala para o eixo X:')
        fator_y = simpledialog.askfloat('Fator de Escala', 'Digite o fator de escala para o eixo Y:')

        transforma_pontos = []
        for ponto in self.pontos:
            x = ponto[0]
            y = ponto[1]
            novo_x = ponto_x + fator_x * (x - ponto_x)
            novo_y = ponto_y + fator_y * (y - ponto_y)
            transforma_pontos.append((novo_x, novo_y))

        self.canvas.create_polygon(
            [self.ponto_fixo] + transforma_pontos, outline='red', fill='')

    def pergunta_transformacao(self):
        resposta = messagebox.askyesno('Nova Transformação', 'Deseja fazer uma nova transformação em escala?')
        if resposta:
            self.pontos = []  # Reseta a lista de pontos
            self.ponto_fixo = None  # Limpa o ponto fixo
            self.canvas.delete('all')  # Remove todos os desenhos do canvas
            self.redesenha_borda()  # Redesenha a borda vermelha
            self.desenha_grid()  # Adiciona o grid novamente
            # Habilita o evento de clique novamente
            self.canvas.bind('<Button-1>', self.desenha_ponto)
        else:
            self.master.quit()

    def redesenha_borda(self):
        self.canvas.create_rectangle(2, 2, 400, 400, outline='red', width=2)

    def desenha_grid(self):
        for x in range(0, 401, 20):
            self.canvas.create_line(x, 0, x, 400, fill='gray')
        for y in range(0, 401, 20):
            self.canvas.create_line(0, y, 400, y, fill='gray')

janela = tk.Tk()
DesenhaRetangulo(janela)
janela.title('Desenho transformado com escala')
janela.mainloop()