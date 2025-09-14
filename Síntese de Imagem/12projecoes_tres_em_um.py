import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button

# Define as coordenadas dos vértices do cubo
vertices = np.array([
    [0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0],
    [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]
])

# Define as arestas do cubo
arestas = np.array([
    [0, 1], [1, 2], [2, 3], [3, 0],
    [4, 5], [5, 6], [6, 7], [7, 4],
    [0, 4], [1, 5], [2, 6], [3, 7]
])

# Vértices originais para reset
vertices_originais = vertices.copy()

# Função do algoritmo de Bresenham para linhas 3D
def bresenham_linha_3d(x0, y0, z0, x1, y1, z1):
    pontos = []
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    dz = abs(z1 - z0)
    xs = 1 if x1 > x0 else -1
    ys = 1 if y1 > y0 else -1
    zs = 1 if z1 > z0 else -1
    
    # Eixo de condução é o eixo X
    if dx >= dy and dx >= dz:
        p1 = 2 * dy - dx
        p2 = 2 * dz - dx
        while x0 != x1:
            x0 += xs
            if p1 >= 0:
                y0 += ys
                p1 -= 2 * dx
            if p2 >= 0:
                z0 += zs
                p2 -= 2 * dx
            p1 += 2 * dy
            p2 += 2 * dz
            pontos.append((x0, y0, z0))
    # Eixo de condução é o eixo Y
    elif dy >= dx and dy >= dz:
        p1 = 2 * dx - dy
        p2 = 2 * dz - dy
        while y0 != y1:
            y0 += ys
            if p1 >= 0:
                x0 += xs
                p1 -= 2 * dy
            if p2 >= 0:
                z0 += zs
                p2 -= 2 * dy
            p1 += 2 * dx
            p2 += 2 * dz
            pontos.append((x0, y0, z0))
    # Eixo de condução é o eixo Z
    else:
        p1 = 2 * dy - dz
        p2 = 2 * dx - dz
        while z0 != z1:
            z0 += zs
            if p1 >= 0:
                y0 += ys
                p1 -= 2 * dz
            if p2 >= 0:
                x0 += xs
                p2 -= 2 * dz
            p1 += 2 * dy
            p2 += 2 * dx
            pontos.append((x0, y0, z0))
    
    return pontos

# Função para desenhar o cubo
def desenhar_cubo(ax, vertices, arestas):
    ax.cla()  # Limpa os eixos
    valores_x = []
    valores_y = []
    valores_z = []
    
    for aresta in arestas:
        pontos = bresenham_linha_3d(
            int(vertices[aresta[0], 0]*100), int(vertices[aresta[0], 1]*100), int(vertices[aresta[0], 2]*100),
            int(vertices[aresta[1], 0]*100), int(vertices[aresta[1], 1]*100), int(vertices[aresta[1], 2]*100)
        )
        for ponto in pontos:
            valores_x.append(ponto[0] / 100.0)
            valores_y.append(ponto[1] / 100.0)
            valores_z.append(ponto[2] / 100.0)
    
    ax.scatter(valores_x, valores_y, valores_z, c='k', marker='o')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Cubo 3 em 1')

# Função para mostrar a projeção ortogonal frontal
def mostrar_projecao_frontal(event):
    ax.view_init(elev=0, azim=0)
    desenhar_cubo(ax, vertices, arestas)
    plt.draw()

# Função para mostrar a projeção perspectiva
def mostrar_projecao_perspectiva(event):
    ax.view_init(elev=30, azim=30)
    desenhar_cubo(ax, vertices, arestas)
    plt.draw()

# Função para mostrar a projeção oblíqua cavalier
def mostrar_projecao_obliqua(event):
    for i in range(vertices.shape[0]):
        x, y, z = vertices[i]
        vertices[i] = [x + z, y + z, z]
    desenhar_cubo(ax, vertices, arestas)
    plt.draw()

# Função para resetar o cubo
def resetar_cubo(event, vertices_ref, vertices_originais_ref):
    vertices_ref[:] = vertices_originais_ref
    mostrar_projecao_perspectiva(event)

# Cria a figura e os eixos 3D
figura = plt.figure(figsize=(8, 6))
ax = figura.add_subplot(111, projection='3d')

# Desenha o cubo inicialmente com projeção perspectiva
desenhar_cubo(ax, vertices, arestas)

# Posições dos botões
botao_frontal_ax = plt.axes([0.05, 0.05, 0.2, 0.075])
botao_perspectiva_ax = plt.axes([0.3, 0.05, 0.2, 0.075])
botao_obliqua_ax = plt.axes([0.55, 0.05, 0.25, 0.075])
botao_reset_ax = plt.axes([0.85, 0.05, 0.1, 0.075])

# Criação dos botões
botao_frontal = Button(botao_frontal_ax, 'Ortog. Frontal', color='lightgoldenrodyellow', hovercolor='lightgray')
botao_perspectiva = Button(botao_perspectiva_ax, 'Perspectiva', color='lightblue', hovercolor='lightgray')
botao_obliqua = Button(botao_obliqua_ax, 'Oblíqua', color='lightgreen', hovercolor='lightgray')
botao_reset = Button(botao_reset_ax, 'Reset', color='lightcoral', hovercolor='lightgray')

# Vincula as funções aos cliques dos botões
botao_frontal.on_clicked(mostrar_projecao_frontal)
botao_perspectiva.on_clicked(mostrar_projecao_perspectiva)
botao_obliqua.on_clicked(mostrar_projecao_obliqua)
botao_reset.on_clicked(lambda event: resetar_cubo(event, vertices, vertices_originais))

plt.show()