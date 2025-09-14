import tkinter as tk
from tkinter import messagebox

# Constantes para os lados do retângulo de recorte
dentro = 0    # 0000
esquerda = 1  # 0001
direita = 2   # 0010
baixo = 4     # 0100
cima = 8      # 1000

# Função para calcular o código de recorte de um ponto
def calcula_recorte(x, y, xmin, ymin, xmax, ymax):
    code = dentro
    if x < xmin:
        code |= esquerda
    elif x > xmax:
        code |= direita
    if y < ymin:
        code |= baixo
    elif y > ymax:
        code |= cima
    return code

# Função para recortar a linha utilizando o algoritmo de Cohen-Sutherland
def recorta_cohensutherland(x1, y1, x2, y2, xmin, ymin, xmax, ymax):
    coord1 = calcula_recorte(x1, y1, xmin, ymin, xmax, ymax)
    coord2 = calcula_recorte(x2, y2, xmin, ymin, xmax, ymax)
    aceita = False

    while True:
        if coord1 == 0 and coord2 == 0:  # Ambos pontos dentro da janela
            aceita = True
            break
        elif coord1 & coord2 != 0:  # Ambos pontos fora da janela em uma mesma região
            break
        else:
            x = 0
            y = 0
            calc_fora = coord1 if coord1 != 0 else coord2

            if calc_fora & cima:
                x = x1 + (x2 - x1) * (ymax - y1) / (y2 - y1)
                y = ymax
            elif calc_fora & baixo:
                x = x1 + (x2 - x1) * (ymin - y1) / (y2 - y1)
                y = ymin
            elif calc_fora & direita:
                y = y1 + (y2 - y1) * (xmax - x1) / (x2 - x1)
                x = xmax
            elif calc_fora & esquerda:
                y = y1 + (y2 - y1) * (xmin - x1) / (x2 - x1)
                x = xmin

            if calc_fora == coord1:
                x1 = x
                y1 = y
                coord1 = calcula_recorte(x1, y1, xmin, ymin, xmax, ymax)
            else:
                x2 = x
                y2 = y
                coord2 = calcula_recorte(x2, y2, xmin, ymin, xmax, ymax)

    if aceita:
        # Desenha a linha recortada
        canvas.create_line(x1, y1, x2, y2, fill='blue')

# Função para recortar o triângulo utilizando o algoritmo de Cohen-Sutherland
def recorta_triangulo(pontos, xmin, ymin, xmax, ymax):
    recortado = []
    for i in range(3):
        x1, y1 = pontos[i * 2], pontos[i * 2 + 1]
        x2, y2 = pontos[(i * 2 + 2) % 6], pontos[(i * 2 + 3) % 6]
        linha_recortada = recorta_cohensutherland(x1, y1, x2, y2, xmin, ymin, xmax, ymax)
        if linha_recortada:
            recortado.extend(linha_recortada[:2])
            recortado.extend(linha_recortada[2:])
    return recortado

# Função para desenhar um triângulo
def desenha_triangulo(x, y, tamanho=50):
    pontos = [
        x, y - tamanho,
        x - tamanho, y + tamanho,
        x + tamanho, y + tamanho
    ]
    pontos_recortados = recorta_triangulo(pontos, xmin, ymin, xmax, ymax)
    if pontos_recortados:
        canvas.create_polygon(pontos_recortados, outline='blue', fill='')

# Função para lidar com a escolha do usuário
def escolha_usuario():
    escolha = opcao.get()
    if escolha == "Linha":
        canvas.bind('<Button-1>', desenha_linha)
    elif escolha == "Triângulo":
        canvas.bind('<Button-1>', desenha_triangulo_evento)

# Função para desenhar uma linha quando selecionada
def desenha_linha(event):
    global ponto_inicial
    x = event.x
    y = event.y
    if ponto_inicial is None:
        ponto_inicial = (x, y)
    else:
        x1, y1 = ponto_inicial
        recorta_cohensutherland(x1, y1, x, y, xmin, ymin, xmax, ymax)
        ponto_inicial = None

# Função para desenhar um triângulo quando selecionado
def desenha_triangulo_evento(event):
    x = event.x
    y = event.y
    desenha_triangulo(x, y)

# Configurações da janela e do canvas
janela = tk.Tk()
janela.title('Recorte Linha e Triângulo')
canvas = tk.Canvas(janela, width=500, height=500)
canvas.pack()

# Limites da janela de recorte
xmin = 100
ymin = 100
xmax = 400
ymax = 400

def desenha_grid():
    tam_grid = 10  # Tamanho de cada célula do grid
    for x in range(xmin, xmax+1, tam_grid):
        canvas.create_line(x, ymin, x, ymax, fill='gray')
    for y in range(ymin, ymax+1, tam_grid):
        canvas.create_line(xmin, y, xmax, y, fill='gray')

# Chama a função para desenhar o grid
desenha_grid()

# Desenha a janela de recorte
canvas.create_rectangle(xmin, ymin, xmax, ymax, outline='red')

# Variável para armazenar o primeiro ponto clicado
ponto_inicial = None

# Opções de escolha (Linha ou Triângulo)
opcao = tk.StringVar()
#opcao.set("Linha")  # Opção padrão

# Radio buttons para seleção
tk.Radiobutton(janela, text="Linha", variable=opcao, value="Linha", command=escolha_usuario).pack(anchor=tk.W)
tk.Radiobutton(janela, text="Triângulo", variable=opcao, value="Triângulo", command=escolha_usuario).pack(anchor=tk.W)

# Executa o loop principal da janela
janela.mainloop()