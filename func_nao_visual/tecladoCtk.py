from customtkinter import *
import pyautogui as py
import time

class TecladoVarreduraTab(CTk):
    def __init__(self):
        super().__init__()
        self.title("Teclado de Varredura")
        self.resizable(False, False)

        self.layout_completo = [
            ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'Backspace'],
            ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
            ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Digitar Texto'],
            ['Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', 'Espaço'],
        ]

        self.entrada = CTkEntry(self, width=600, height=35, font=('Arial', 14))
        self.entrada.pack(padx=10, pady=5)

        botao_enviar = CTkButton(self, text="Digitar Texto", width=150, height=40, font=('Arial', 12),
                                 command=self.enviar_texto)
        botao_enviar.pack(pady=5)

        self.frame_teclado = CTkFrame(self, fg_color="transparent")
        self.frame_teclado.pack(padx=10, pady=10)

        self.botoes = []
        self.indice_tab = 0 
        self.tab_direcao = 1  
        self.carregar_teclas()

        # Bind do Tab e setas
        self.bind("<Tab>", self.tab_seguinte)
        self.bind("<Return>", self.confirmar_tecla)
        self.bind("<Left>", lambda e: self.mudar_direcao(-1))
        self.bind("<Right>", lambda e: self.mudar_direcao(1))
        self.focus_force()

        self.destacar_tecla(self.indice_tab)

    def carregar_teclas(self):
        for widget in self.frame_teclado.winfo_children():
            widget.destroy()

        self.botoes.clear()
        for r_idx, linha in enumerate(self.layout_completo):
            for c_idx, tecla in enumerate(linha):
                botao = CTkButton(self.frame_teclado, text=tecla, width=50, height=40,
                                  command=lambda t=tecla: self.adicionar_a_entrada(t))
                botao.grid(row=r_idx, column=c_idx, padx=2, pady=2)
                self.botoes.append(botao)

    def tab_seguinte(self, event=None):
        self.remover_destaque(self.indice_tab)
        self.indice_tab += self.tab_direcao

        if self.indice_tab >= len(self.botoes):
            self.indice_tab = 0
        elif self.indice_tab < 0:
            self.indice_tab = len(self.botoes) - 1

        self.destacar_tecla(self.indice_tab)
        return "break"  

    def mudar_direcao(self, direcao):
        self.tab_direcao = direcao

    def destacar_tecla(self, idx):
        botao = self.botoes[idx]
        botao.configure(border_width=3, border_color="red")

    def remover_destaque(self, idx):
        botao = self.botoes[idx]
        botao.configure(border_width=0)

    def confirmar_tecla(self, event=None):
        tecla = self.botoes[self.indice_tab].cget("text")
        self.adicionar_a_entrada(tecla)

    def adicionar_a_entrada(self, tecla):
        if tecla == 'Backspace':
            self.entrada.delete(len(self.entrada.get()) - 1, END)
        elif tecla == 'Espaço':
            self.entrada.insert(END, ' ')
        elif tecla == 'Digitar Texto':
            self.enviar_texto()
        else:
            self.entrada.insert(END, tecla)

    def enviar_texto(self):
        texto_para_digitar = self.entrada.get()
        if not texto_para_digitar:
            return

        self.withdraw()
        time.sleep(1)
        py.write(texto_para_digitar, interval=0.05)
        self.deiconify()
        self.entrada.delete(0, END)
        self.focus_force()


if __name__ == "__main__":
    set_appearance_mode("System")
    set_default_color_theme("blue")
    app = TecladoVarreduraTab()
    app.mainloop()