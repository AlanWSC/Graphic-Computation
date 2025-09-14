import tkinter as tk

class PreenchimentoRecursivoApp:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Preenchimento Recursivo")
        
        # Dicionário que mapeia valores numéricos para cores específicas
        self.mapa_cores = {0: "white", 1: "black", 2: "blue", 3: "red"}

        # Cor utilizada para preenchimento
        self.cor_substituta = 3
        self.tamanho_celula = 30
        
        # Criação do canvas
        self.canvas = tk.Canvas(janela, width=20 * self.tamanho_celula, height=10 * self.tamanho_celula)
        self.canvas.pack()
        

        # Botão para resetar a imagem
        self.botao_resetar = tk.Button(janela, text="Resetar", command=self.resetar_imagem)
        self.botao_resetar.pack()
        
        self.resetar_imagem()

    # Algoritmo de preenchimento recursivo.
    def preenchimento_recursivo(self, x, y, cor_alvo):

        # Condições de parada da recursão
        if x < 0 or x >= len(self.imagem[0]) or y < 0 or y >= len(self.imagem):
            return
        if self.imagem[y][x] != cor_alvo:
            return
        if self.imagem[y][x] == self.cor_substituta:
            return

        # Substitui a cor na posição (x, y) pela cor de substituição
        self.imagem[y][x] = self.cor_substituta
        # Atualiza a cor da célula correspondente no canvas
        self.canvas.itemconfig(self.celulas[y][x], fill=self.mapa_cores[self.cor_substituta])

        # Chama recursivamente o preenchimento para os vizinhos
        self.preenchimento_recursivo(x + 1, y, cor_alvo)
        self.preenchimento_recursivo(x - 1, y, cor_alvo)
        self.preenchimento_recursivo(x, y + 1, cor_alvo)
        self.preenchimento_recursivo(x, y - 1, cor_alvo)

    # Eventos de clique no canvas.
    def ao_clicar(self, evento):
        
        # Calcula as coordenadas (x, y) da célula clicada
        x = evento.x // self.tamanho_celula
        y = evento.y // self.tamanho_celula

        if evento.num == 1:  # Clique esquerdo
            cor_alvo = self.imagem[y][x] # Obtém a cor da célula clicada
            if cor_alvo != self.cor_substituta:

                # Inicia o preenchimento recursivo se a cor não for a cor de substituição
                self.preenchimento_recursivo(x, y, cor_alvo)

    def resetar_imagem(self):
        self.imagem = [
            [1, 1, 1, 2, 2, 1, 1, 1, 0, 0, 1, 2, 1, 1, 1, 2, 2, 1, 1, 1],
            [1, 1, 0, 2, 2, 0, 1, 1, 0, 0, 2, 1, 0, 1, 1, 0, 2, 2, 0, 1],
            [1, 0, 0, 2, 2, 1, 0, 1, 0, 0, 1, 2, 1, 1, 0, 2, 2, 1, 0, 1],
            [2, 2, 0, 0, 0, 1, 0, 1, 1, 1, 2, 1, 0, 1, 0, 0, 0, 1, 0, 1],
            [2, 2, 2, 0, 0, 0, 1, 1, 1, 1, 1, 2, 1, 0, 2, 2, 0, 0, 0, 1],
            [1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 2, 1, 0, 1, 1, 0, 1, 1, 1, 0],
            [1, 1, 0, 2, 2, 0, 0, 0, 0, 0, 1, 2, 1, 1, 0, 2, 2, 0, 0, 1],
            [1, 0, 0, 2, 2, 1, 0, 0, 0, 0, 2, 1, 0, 1, 0, 0, 0, 1, 0, 1],
            [2, 2, 0, 0, 0, 1, 1, 1, 0, 0, 1, 2, 1, 0, 2, 2, 0, 0, 0, 1],
            [2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 2, 1, 0, 1, 1, 1, 0, 0, 0, 1],
        ]
        self.redesenhar_canvas()

    def redesenhar_canvas(self):
        self.canvas.delete("all")  # Limpa o canvas
        self.celulas = []
        for y, linha in enumerate(self.imagem):
            linha_celulas = []
            for x, cor in enumerate(linha):
                # Cria um retângulo (célula) na posição atual do grid
                celula = self.canvas.create_rectangle(x * self.tamanho_celula, y * self.tamanho_celula, (x + 1) * self.tamanho_celula, (y + 1) * self.tamanho_celula, fill=self.mapa_cores[cor], outline="black")
                linha_celulas.append(celula)  # Adiciona a célula à linha atual
                self.canvas.tag_bind(celula, "<Button-1>", self.ao_clicar)  # Liga o evento de clique esquerdo à célula
            self.celulas.append(linha_celulas)  # Adiciona a linha de células à lista de células

# Criação da janela principal
janela = tk.Tk()
app = PreenchimentoRecursivoApp(janela)
janela.mainloop()