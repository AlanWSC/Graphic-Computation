import tkinter as tk

def circulo(xc, yc, r):
    x = 0
    y = r
    p = 3 - 2 * r

    desenha_circulo(xc, yc, x, y)

    while x <= y:
        x += 1
        if p < 0:
            p += 4 * x + 6
        else:
            y -= 1
            p += 4 * (x - y) + 10
        desenha_circulo(xc, yc, x, y)

def desenha_circulo(xc, yc, x, y):
    canvas.create_rectangle(xc + x, yc + y, xc + x + 1,
                            yc + y + 1, fill='black')
    canvas.create_rectangle(xc - x, yc + y, xc - x + 1,
                            yc + y + 1, fill='black')
    canvas.create_rectangle(xc + x, yc - y, xc + x + 1,
                            yc - y + 1, fill='black')
    canvas.create_rectangle(xc - x, yc - y, xc - x + 1,
                            yc - y + 1, fill='black')
    canvas.create_rectangle(xc + y, yc + x, xc + y + 1,
                            yc + x + 1, fill='black')
    canvas.create_rectangle(xc - y, yc + x, xc - y + 1,
                            yc + x + 1, fill='black')
    canvas.create_rectangle(xc + y, yc - x, xc + y + 1,
                            yc - x + 1, fill='black')
    canvas.create_rectangle(xc - y, yc - x, xc - y + 1,
                            yc - x + 1, fill='black')

def desenha_grid():
    for i in range(0, 500, 20):
        canvas.create_line(i, 0, i, 500, fill='gray')
        canvas.create_line(0, i, 500, i, fill='gray')

def clique(event):
    global xc, yc, r
    if not xc and not yc:
        xc, yc = event.x, event.y
        desenha_grid()
        return
    if xc and yc and not r:
        r = ((event.x - xc) ** 2 + (event.y - yc) ** 2) ** 0.5
        circulo(xc, yc, int(r))
        xc, yc, r = None, None, None

janela = tk.Tk()
janela.title('Desenho de círculo')
canvas = tk.Canvas(janela, width=500, height=500)
canvas.pack()

xc, yc, r = None, None, None

canvas.bind('<Button-1>', clique)

janela.mainloop()