import tkinter as tk

class desenha_retang:
    def __init__(self, master):
        self.master = master
        self.canvas = tk.Canvas(self.master, width=400, height=400)
        self.canvas.pack()

        self.pontos = []
        self.poligono = []

        self.canvas.bind('<Button-1>', self.adiciona_ponto)
        self.canvas.bind('<Button-3>', self.verifica_ponto)

        self.desenha_grid()  # Adiciona a chamada para desenhar o grid

    def desenha_grid(self):
        for i in range(0, 400, 20):  # Desenha linhas verticais
            self.canvas.create_line(i, 0, i, 400, fill='lightgray')
        for i in range(0, 400, 20):  # Desenha linhas horizontais
            self.canvas.create_line(0, i, 400, i, fill='lightgray')

    def adiciona_ponto(self, event):
        x, y = event.x, event.y
        self.pontos.append((x, y))
        self.canvas.create_oval(x-2, y-2, x+2, y+2, fill='black')

        if len(self.pontos) > 1:
            self.canvas.create_line(self.pontos[-2], self.pontos[-1])

    def verifica_ponto(self, event):
        if len(self.pontos) > 2:
            self.poligono.append(list(self.pontos))
            self.preenche_cor()
            self.pontos = []

    def preenche_cor(self):
        min_y = min(pt[1] for pt in self.pontos)
        max_y = max(pt[1] for pt in self.pontos)

        for y in range(min_y, max_y + 1):
            intersecao = []
            for i in range(len(self.pontos)):
                x1, y1 = self.pontos[i]
                x2, y2 = self.pontos[(i + 1) % len(self.pontos)]

                if y1 <= y < y2 or y2 <= y < y1:
                    x_intersecao = int(x1 + (y - y1) * (x2 - x1) / (y2 - y1))
                    intersecao.append(x_intersecao)

            intersecao.sort()
            for i in range(0, len(intersecao), 2):
                x1, x2 = intersecao[i], intersecao[i + 1]
                self.canvas.create_line(x1, y, x2, y, fill='blue')

def main():
    janela = tk.Tk()
    desenha_retang(janela)
    janela.title('Desenho de Poligono Preenchido')
    janela.mainloop()

if __name__ == '__main__':
    main()