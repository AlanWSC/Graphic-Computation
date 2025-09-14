import tkinter as tk
from tkinter import simpledialog, messagebox

class DesenhaRetang:
    def __init__(self, master):
        self.master = master
        self.canvas = tk.Canvas(
            self.master, width=400, height=400, bd=2, relief='solid',
            highlightbackground='red')
        self.canvas.pack()
        self.canvas.bind('<Button-1>', self.desenha_ponto)
        self.pontos = []
        self.transla_pontos = []
        self.desenha_grid()

    def desenha_grid(self):
        # Desenha as linhas verticais do grid
        for x in range(0, 400, 20):
            self.canvas.create_line(x, 0, x, 400, fill='lightgray')
        # Desenha as linhas horizontais do grid
        for y in range(0, 400, 20):
            self.canvas.create_line(0, y, 400, y, fill='lightgray')

    def desenha_ponto(self, event):
        x = event.x
        y = event.y
        self.pontos.append((x, y))
        self.canvas.create_oval(x-3, y-3, x+3, y+3, fill='black')

        if len(self.pontos) == 3:
            self.desenha_triangulo()
            self.canvas.unbind('<Button-1>')  # Desabilita o evento de clique
            self.valores_transla()

    def desenha_triangulo(self):
        self.canvas.create_polygon(self.pontos, outline='black', fill='')

    def valores_transla(self):
        while True:
            x = simpledialog.askinteger('Entrada eixo X', 'Insira o valor de deslocamento no eixo x:')
            y = simpledialog.askinteger('Entrada eixo Y', 'Insira o valor de deslocamento no eixo y:')
            self.mov_triangulo(x, y)
            if not messagebox.askyesno('Translação', 'Deseja fazer outra translação do objeto?'):
                break

    def mov_triangulo(self, x, y):
        self.transla_pontos = [(point[0] + x, point[1] + y) for point in self.pontos]
        self.canvas.create_polygon(self.transla_pontos, outline='red', fill='')
        self.pontos = self.transla_pontos  # Atualiza os pontos para a nova posição

janela = tk.Tk()
DesenhaRetang(janela)
janela.title('Desenha com translação')
janela.mainloop()