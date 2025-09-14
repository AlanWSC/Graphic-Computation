import tkinter as tk

class DesenhadorElipse:
    def __init__(self, canvas, linhas, colunas, tamanho_celula):
        self.canvas = canvas
        self.linhas = linhas
        self.colunas = colunas
        self.tamanho_celula = tamanho_celula
        self.dados_grid = [[0 for _ in range(colunas)] for _ in range(linhas)]
        self.primeiro_clique = None
        self.elipse_temporaria = None

        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

    def desenhar_grid(self):
        for i in range(self.linhas):
            for j in range(self.colunas):
                x0, y0 = j * self.tamanho_celula, i * self.tamanho_celula
                x1, y1 = x0 + self.tamanho_celula, y0 + self.tamanho_celula
                self.canvas.create_rectangle(x0, y0, x1, y1, outline="gray", fill="white")

    def desenhar_elipse_temporaria(self, x0, y0, x1, y1):
        if self.elipse_temporaria:
            self.canvas.delete(self.elipse_temporaria)
        self.elipse_temporaria = self.canvas.create_oval(x0, y0, x1, y1, outline="black", width=2, dash=(2, 2))

    def desenhar_elipse(self, x0, y0, x1, y1):
        a = abs(x1 - x0) // 2
        b = abs(y1 - y0) // 2
        xc = (x0 + x1) // 2
        yc = (y0 + y1) // 2

        x = 0
        y = b
        d1 = ((b*b) - (a*a*b) + (0.25*a*a))
        dx = 2*b*b*x
        dy = 2*a*a*y

        while dx < dy:
            self.desenhar_pontos_elipse(x, y, xc, yc)
            if d1 < 0:
                x += 1
                dx = dx + (2 * b * b)
                d1 = d1 + dx + (b * b)
            else:
                x += 1
                y -= 1
                dx = dx + (2 * b * b)
                dy = dy - (2 * a * a)
                d1 = d1 + dx - dy + (b * b)
                
        d2 = (((b*b)*(x+0.5)*(x+0.5)) + ((a*a)*(y-1)*(y-1)) - (a*a*b*b))
        while y >= 0:
            self.desenhar_pontos_elipse(x, y, xc, yc)
            if d2 > 0:
                y -= 1
                dy = dy - (2 * a * a)
                d2 = d2 - dy + (a * a)
            else:
                x += 1
                y -= 1
                dy = dy - (2 * a * a)
                dx = dx + (2 * b * b)
                d2 = d2 + dx - dy + (a * a)
        
    def desenhar_pontos_elipse(self, x, y, xc, yc):
        self.desenhar_celula(xc + x, yc + y)
        self.desenhar_celula(xc - x, yc + y)
        self.desenhar_celula(xc + x, yc - y)
        self.desenhar_celula(xc - x, yc - y)

    def desenhar_celula(self, coluna, linha):
        if 0 <= coluna < self.colunas and 0 <= linha < self.linhas:
            x0, y0 = coluna * self.tamanho_celula, linha * self.tamanho_celula
            x1, y1 = x0 + self.tamanho_celula, y0 + self.tamanho_celula
            self.canvas.create_rectangle(x0, y0, x1, y1, outline="", fill="black")
            self.dados_grid[linha][coluna] = 1

    def on_click(self, event):
        coluna = event.x // self.tamanho_celula
        linha = event.y // self.tamanho_celula

        if self.primeiro_clique is None:
            self.primeiro_clique = (coluna, linha)
        else:
            segundo_clique = (coluna, linha)
            self.desenhar_elipse(self.primeiro_clique[0], self.primeiro_clique[1], segundo_clique[0], segundo_clique[1])
            self.primeiro_clique = None

    def on_drag(self, event):
        if self.primeiro_clique:
            coluna = event.x // self.tamanho_celula
            linha = event.y // self.tamanho_celula
            x0, y0 = self.primeiro_clique[0] * self.tamanho_celula, self.primeiro_clique[1] * self.tamanho_celula
            x1, y1 = (coluna + 1) * self.tamanho_celula, (linha + 1) * self.tamanho_celula
            self.desenhar_elipse_temporaria(x0, y0, x1, y1)

    def on_release(self, event):
        if self.elipse_temporaria:
            self.canvas.delete(self.elipse_temporaria)

class Aplicacao:
    def __init__(self, mestre, linhas=20, colunas=20, tamanho_celula=15):
        self.mestre = mestre
        self.linhas = linhas
        self.colunas = colunas
        self.tamanho_celula = tamanho_celula

        self.canvas = tk.Canvas(mestre, width=colunas*tamanho_celula, height=linhas*tamanho_celula)
        self.canvas.pack()

        self.desenhador_elipse = DesenhadorElipse(self.canvas, linhas, colunas, tamanho_celula)
        self.desenhador_elipse.desenhar_grid()

janela = tk.Tk()
janela.title('Desenho Elipse')
app = Aplicacao(janela, linhas=30, colunas=30, tamanho_celula=15)
janela.mainloop()