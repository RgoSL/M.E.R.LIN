import time
import tkinter as tk

import pyautogui


class TecladoVarredura(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Teclado de Varredura")
        self.resizable(False, False)

        # Layout completo do teclado
        self.layout_completo = [
            ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "Backspace"],
            ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
            ["A", "S", "D", "F", "G", "H", "J", "K", "L", "Enter"],
            ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "Espaço"],
        ]

        self.historico = []
        self.texto_digitado = ""

        self.entrada = tk.Entry(self, width=60, font=("Arial", 14))
        self.entrada.pack(padx=10, pady=5)

        botao_enviar = tk.Button(
            self,
            text="Digitar Texto",
            width=15,
            height=2,
            font=("Arial", 12),
            command=self.enviar_texto,
        )
        botao_enviar.pack(pady=5)

        self.frame_teclado = tk.Frame(self)
        self.frame_teclado.pack(padx=10, pady=10)

        # Cria um Canvas para desenhar as bordas
        self.canvas = tk.Canvas(
            self.frame_teclado, highlightthickness=0, bg="SystemButtonFace"
        )
        # Coloca o Canvas na primeira linha e coluna com um grande colspan/rowspan
        # para que ele ocupe todo o espaço do grid, mas por baixo dos botões.
        self.canvas.grid(row=0, column=0, rowspan=5, columnspan=12, sticky="nsew")
        self.canvas_rect_id = None

        self.botoes = {}
        self.carregar_teclas(self.layout_completo)

        self.bind("<Up>", lambda e: self.selecionar_quadrante(0))
        self.bind("<Right>", lambda e: self.selecionar_quadrante(1))
        self.bind("<Down>", lambda e: self.selecionar_quadrante(2))
        self.bind("<Left>", lambda e: self.selecionar_quadrante(3))
        self.bind("<Return>", self.confirmar_selecao)

        self.focus_force()

    def carregar_teclas(self, layout):
        """Limpa o frame e desenha o novo conjunto de botões."""
        self.canvas.delete("all")
        for widget in self.frame_teclado.winfo_children():
            # Apenas destrói os botões, não o canvas.
            if widget != self.canvas:
                widget.destroy()

        self.botoes = {}

        row_offset = 0
        if layout != self.layout_completo:
            botao_voltar = tk.Button(
                self.frame_teclado,
                text="Voltar",
                width=10,
                height=2,
                command=self.voltar,
            )
            botao_voltar.grid(
                row=0,
                column=0,
                columnspan=max(len(row) for row in layout) + 1,
                padx=2,
                pady=2,
                sticky="ew",
            )
            self.botoes["Voltar"] = botao_voltar
            row_offset = 1

        for r_idx, linha in enumerate(layout):
            for c_idx, tecla in enumerate(linha):
                botao = tk.Button(
                    self.frame_teclado,
                    text=tecla,
                    width=5,
                    height=2,
                    command=lambda t=tecla: self.adicionar_a_entrada(t),
                )
                botao.grid(row=r_idx + row_offset, column=c_idx, padx=2, pady=2)
                self.botoes[tecla] = botao

        self.update_idletasks()
        bbox = self.frame_teclado.grid_bbox(
            0, 0, self.frame_teclado.grid_size()[0], self.frame_teclado.grid_size()[1]
        )
        if bbox:
            width = bbox[2] - bbox[0]
            height = bbox[3] - bbox[1]
            self.canvas.config(width=width, height=height)

    def desenhar_borda_quadrante(self, layout_quadrante):
        """Desenha uma borda em torno do quadrante atual no canvas."""
        self.canvas.delete(self.canvas_rect_id)

        if not layout_quadrante or not self.botoes:
            self.canvas_rect_id = None
            return

        primeira_tecla = layout_quadrante[0][0]
        ultima_linha = layout_quadrante[-1]
        ultima_tecla = ultima_linha[-1]

        if primeira_tecla not in self.botoes or ultima_tecla not in self.botoes:
            self.canvas_rect_id = None
            return

        botao_inicio = self.botoes[primeira_tecla]
        botao_fim = self.botoes[ultima_tecla]

        x1 = botao_inicio.winfo_x() + botao_inicio.winfo_width() / 2
        y1 = botao_inicio.winfo_y() + botao_inicio.winfo_height() / 2
        x2 = botao_fim.winfo_x() + botao_fim.winfo_width() / 2
        y2 = botao_fim.winfo_y() + botao_fim.winfo_height() / 2

        padding_x = 25
        padding_y = 20

        self.canvas_rect_id = self.canvas.create_rectangle(
            x1 - padding_x,
            y1 - padding_y,
            x2 + padding_x,
            y2 + padding_y,
            outline="red",
            width=3,
        )
        self.canvas.tag_raise(self.canvas_rect_id)

    def selecionar_quadrante(self, quadrante_idx):
        layout_atual = self.historico[-1] if self.historico else self.layout_completo

        metade_linhas = (len(layout_atual) + 1) // 2

        novas_linhas = []
        for linha in layout_atual:
            metade_colunas = (len(linha) + 1) // 2

            if quadrante_idx == 0:
                nova_linha = linha[:metade_colunas]
            elif quadrante_idx == 1:
                nova_linha = linha[metade_colunas:]
            elif quadrante_idx == 2:
                nova_linha = linha[metade_colunas:]
            else:
                nova_linha = linha[:metade_colunas]

            if nova_linha:
                novas_linhas.append(nova_linha)

        if quadrante_idx <= 1:
            novo_layout = novas_linhas[:metade_linhas]
        else:
            novo_layout = novas_linhas[metade_linhas:]

        novo_layout = [linha for linha in novo_layout if linha]
        if not novo_layout:
            return

        self.historico.append(novo_layout)
        self.carregar_teclas(novo_layout)

        self.after(100, lambda: self.desenhar_borda_quadrante(novo_layout))

    def confirmar_selecao(self, event=None):
        if len(self.historico) > 0:
            layout_atual = self.historico[-1]
            if len(layout_atual) == 1 and len(layout_atual[0]) == 1:
                tecla = layout_atual[0][0]
                self.adicionar_a_entrada(tecla)
                self.historico = []
                self.carregar_teclas(self.layout_completo)
            else:
                pass

    def adicionar_a_entrada(self, tecla):
        if tecla == "Backspace":
            self.entrada.delete(len(self.entrada.get()) - 1, tk.END)
        elif tecla == "Espaço":
            self.entrada.insert(tk.END, " ")
        elif tecla == "Enter":
            self.enviar_texto()
        else:
            self.entrada.insert(tk.END, tecla)

    def enviar_texto(self):
        """Esconde a janela, digita o texto e a reexibe."""
        texto_para_digitar = self.entrada.get()
        if not texto_para_digitar:
            return

        self.withdraw()
        time.sleep(2)

        pyautogui.write(texto_para_digitar, interval=0.05)

        self.deiconify()
        self.entrada.delete(0, tk.END)
        self.focus_force()

    def voltar(self):
        """Volta para o layout anterior na pilha."""
        if len(self.historico) > 1:
            self.historico.pop()
            self.carregar_teclas(self.historico[-1])
            self.after(100, lambda: self.desenhar_borda_quadrante(self.historico[-1]))
        else:
            self.historico = []
            self.carregar_teclas(self.layout_completo)


if __name__ == "__main__":
    app = TecladoVarredura()
    app.mainloop()
