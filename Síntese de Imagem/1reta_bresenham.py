import tkinter as tk

class desenha_retang:
    def __init__(self, master):
        self.master = master
        self.master.title('Desenho de reta com Bresenham')

        # Cria o canvas
        self.canvas = tk.Canvas(
            self.master, width=500, height=500)
        self.canvas.pack()

        # Desenha grid
        for x in range(0, 500, 5):
            self.canvas.create_line(x, 0, x, 500, fill='white')
        for y in range(0, 500, 5):
            self.canvas.create_line(0, y, 500, y, fill='white')

        # Variáveis para armazenar as coordenadas do ponto
        # Inicial e final da reta

        self.inicia_x = None
        self.inicia_y = None
        self.fim_x = None
        self.fim_y = None

        # Bind dos eventos do mouse
        self.canvas.bind("<Button-1>", self.clique_inicial)
        self.canvas.bind("<B1-Motion>", self.clique_final)
        self.canvas.bind("<ButtonRelease-1>", self.solta_clique)

    def clique_inicial(self, event):
        # Armazena as coordenadas do ponto inicial
        self.inicio_x = round(event.x / 5) * 5
        self.inicio_y = round(event.y / 5) * 5

    def clique_final(self, event):
        # Atualiza as coordenadas do ponto final enquanto o mouse se movegp
        self.fim_x = round(event.x / 5) * 5
        self.fim_y = round(event.y / 5) * 5
        self.desenha_linha()

    def solta_clique(self, event):
        # Desenha a linha final
        self.fim_x = round(event.x / 5) * 5
        self.fim_y = round(event.y / 5) * 5
        self.desenha_linha()

    def desenha_linha(self):

        self.canvas.delete('linha')  # Remove a linha anterior

        # Desenha a linha usando o algoritmo de Bresenham
        x0, y0, x1, y1 = self.inicio_x, self.inicio_y, self.fim_x, self.fim_y
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy

        while True:
            self.canvas.create_rectangle(
                x0, y0, x0 + 5, y0 + 5, fill='black', tags='linha')
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

# Cria a janela principal
janela = tk.Tk()

# Cria o objeto de desenho de retas
desenha_retang(janela)

# Inicia o loop principal da aplicação
janela.mainloop()