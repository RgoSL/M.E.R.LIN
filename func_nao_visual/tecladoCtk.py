from customtkinter import *
import pyautogui as py
import time

class TecladoVarredura(CTk):
    def __init__(self):
        super().__init__()
        self.title("Teclado de Varredura")
        self.resizable(False, False)

        # Layout completo do teclado
        self.layout_completo = [
            ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'Backspace'],
            ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
            ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Enter'],
            ['Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', 'Espaço'],
        ]

        self.historico = []

        # Entrada customizada
        self.entrada = CTkEntry(self, width=600, height=35, font=('Arial', 14))
        self.entrada.pack(padx=10, pady=5)

        botao_enviar = CTkButton(self, text="Digitar Texto", width=150, height=40, font=('Arial', 12),
                                     command=self.enviar_texto)
        botao_enviar.pack(pady=5)

        self.frame_teclado = CTkFrame(self, fg_color="transparent")
        self.frame_teclado.pack(padx=10, pady=10)

        self.botoes = {}
        self.borda_quadrante = None
        self.carregar_teclas(self.layout_completo)

        self.bind("<Up>", lambda e: self.selecionar_quadrante(0))
        self.bind("<Right>", lambda e: self.selecionar_quadrante(1))
        self.bind("<Down>", lambda e: self.selecionar_quadrante(2))
        self.bind("<Left>", lambda e: self.selecionar_quadrante(3))
        self.bind("<Return>", self.confirmar_selecao)

        self.focus_force()

    def carregar_teclas(self, layout):
        """Limpa o frame e desenha o novo conjunto de botões."""
        for widget in self.frame_teclado.winfo_children():
            widget.destroy()

        self.botoes = {}

        row_offset = 0
        if layout != self.layout_completo:
            botao_voltar = CTkButton(self.frame_teclado, text="Voltar", width=100, height=40,
                                         command=self.voltar)
            botao_voltar.grid(row=0, column=0, columnspan=max(len(row) for row in layout) + 1, padx=2, pady=2,
                              sticky="ew")
            self.botoes["Voltar"] = botao_voltar
            row_offset = 1

        for r_idx, linha in enumerate(layout):
            for c_idx, tecla in enumerate(linha):
                botao = CTkButton(self.frame_teclado, text=tecla, width=50, height=40,
                                      command=lambda t=tecla: self.adicionar_a_entrada(t))
                botao.grid(row=r_idx + row_offset, column=c_idx, padx=2, pady=2)
                self.botoes[tecla] = botao

    def desenhar_borda_quadrante(self, layout_quadrante):
        """Desenha uma borda em torno do quadrante usando CTkFrame transparente."""
        if self.borda_quadrante:
            self.borda_quadrante.destroy()
            self.borda_quadrante = None

        if not layout_quadrante or not self.botoes:
            return

        primeira_tecla = layout_quadrante[0][0]
        ultima_tecla = layout_quadrante[-1][-1]

        if primeira_tecla not in self.botoes or ultima_tecla not in self.botoes:
            return

        botao_inicio = self.botoes[primeira_tecla]
        botao_fim = self.botoes[ultima_tecla]

        x1, y1 = botao_inicio.winfo_x(), botao_inicio.winfo_y()
        x2 = botao_fim.winfo_x() + botao_fim.winfo_width()
        y2 = botao_fim.winfo_y() + botao_fim.winfo_height()

        padding = 5
        self.borda_quadrante = CTkFrame(self.frame_teclado, fg_color="transparent", border_width=3,
                                           border_color="red")
        self.borda_quadrante.place(x=x1 - padding, y=y1 - padding, width=x2 - x1 + 2 * padding,
                                   height=y2 - y1 + 2 * padding)

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

    def adicionar_a_entrada(self, tecla):
        if tecla == 'Backspace':
            self.entrada.delete(len(self.entrada.get()) - 1, END)
        elif tecla == 'Espaço':
            self.entrada.insert(END, ' ')
        elif tecla == 'Enter':
            self.enviar_texto()
        else:
            self.entrada.insert(END, tecla)

    def enviar_texto(self):
        texto_para_digitar = self.entrada.get()
        if not texto_para_digitar:
            return

        self.withdraw()
        time.sleep(2)
        py.write(texto_para_digitar, interval=0.05)
        self.deiconify()
        self.entrada.delete(0, END)
        self.focus_force()

    def voltar(self):
        if len(self.historico) > 1:
            self.historico.pop()
            self.carregar_teclas(self.historico[-1])
            self.after(100, lambda: self.desenhar_borda_quadrante(self.historico[-1]))
        else:
            self.historico = []
            self.carregar_teclas(self.layout_completo)


if __name__ == "__main__":
    set_appearance_mode("System")  
    set_default_color_theme("blue")  
    app = TecladoVarredura()
    app.mainloop()