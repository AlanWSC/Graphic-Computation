import tkinter as tk

pontos = []  # Lista para armazenar os pontos da polilinha

def desenha_polilinha(event):
    x, y = event.x, event.y
    pontos.append((x, y))  # Adiciona o ponto atual à lista de pontos

    if len(pontos) >= 3:
        # Desenha a polilinha
        canvas.create_line(pontos, fill='black', width=2)

def desenha_grid():
    # Desenha as linhas verticais do grid
    for x in range(0, 400, 20):
        canvas.create_line(x, 0, x, 400, fill='gray', tags="grid")

    # Desenha as linhas horizontais do grid
    for y in range(0, 400, 20):
        canvas.create_line(0, y, 400, y, fill='gray', tags="grid")

janela = tk.Tk()
janela.title("Desenhar Polilinhas")

canvas = tk.Canvas(janela, width=400, height=400)
canvas.pack()

# Liga o evento de clique do mouse à função de desenho
canvas.bind('<Button-1>', desenha_polilinha)

desenha_grid()  # Desenha o grid inicialmente

janela.mainloop()