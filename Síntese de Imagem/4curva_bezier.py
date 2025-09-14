import tkinter as tk

# Inicializa o Tkinter
janela = tk.Tk()

# Cria o canvas
canvas = tk.Canvas(janela, width=640, height=480, bg='white')
canvas.pack()

# Define os pontos de controle iniciais como vazio
pontos_controle = []

# Define a função para desenhar a curva de Bezier

def desenha_curva_bezier(points):
    # Verifica se há pontos suficientes para desenhar a curva
    if len(points) < 2:
        return

    # Calcula a lista de pontos intermediários na curva de Bezier
    # usando o algoritmo de Bresenham
    x0, y0 = points[0]
    x3, y3 = points[3]

    x = x0
    y = y0

    ponto_curva = [(x, y)]

    t = 0.0
    dt = 1.0 / max(abs(x3 - x0), abs(y3 - y0))

    while t < 1.0:
        t += dt

        x = int((1 - t) ** 3 * x0 + 3 * (1 - t) ** 2 * t *
                points[1][0] + 3 * (1 - t) * t ** 2 * points[2][0] + t ** 3
                * x3 + 0.5)
        y = int((1 - t) ** 3 * y0 + 3 * (1 - t) ** 2 * t *
                points[1][1] + 3 * (1 - t) * t ** 2 * points[2][1] + t **
                3 * y3 + 0.5)

        ponto_curva.append((x, y))

    # Desenha a curva no canvas usando o algoritmo de Bresenham
    x_prev, y_prev = ponto_curva[0]
    for x, y in ponto_curva[1:]:
        canvas.create_line(x_prev, y_prev, x, y, fill='black', width=2)
        x_prev, y_prev = x, y

# Define a função para lidar com cliques do mouse

def clique_mouse(event):
    global pontos_controle

    # Adiciona o ponto de controle à lista de pontos
    pontos_controle.append((event.x, event.y))

    # Se há pelo menos 4 pontos de controle, desenha a curva de Bezier
    if len(pontos_controle) == 4:
        desenha_curva_bezier(pontos_controle)

        # Limpa a lista de pontos de controle
        pontos_controle = []

def desenha_grid():
    # Define o espaçamento entre as linhas do grid
    espaco = 20

    # Desenha as linhas verticais do grid
    for x in range(0, 640, espaco):
        canvas.create_line(x, 0, x, 480, fill='gray', width=1)

    # Desenha as linhas horizontais do grid
    for y in range(0, 480, espaco):
        canvas.create_line(0, y, 640, y, fill='gray', width=1)

# Liga a função de tratamento de cliques do mouse ao evento de clique
canvas.bind('<Button-1>', clique_mouse)

janela.title('Desenho da curva Bezier')

# Desenha o grid
desenha_grid()

# Inicia o loop principal do Tkinter
janela.mainloop()