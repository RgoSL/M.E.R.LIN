from customtkinter import *
from paginas_alt.inicial import inicial
from paginas_alt.esc_config import config
from paginas_alt.video_assis import video_Assis
from paginas_alt.ajustes import ajustes
from paginas_alt.termos_de_uso import termos_de_uso
from paginas_alt.modo_claro_escuro import modo_claro_escuro
from paginas_alt.idioma_software import idioma_software
from paginas_alt.comandos_coletanea import comandos_coletanea


def centralizar_janela(janela, largura, altura):
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()
    x = int((largura_tela / 2) - (largura / 2))
    y = int((altura_tela / 2) - (altura / 2))
    janela.geometry(f"{largura}x{altura}+{x}+{y}")

"""
testando se está commitando
"""
def cor_atual():
    modo = get_appearance_mode()
    return "#FFFFFF" if modo == "Light" else "#2B2B2B"


class App(CTk):
    def __init__(self): 
        super().__init__()
        largura_janela = 800
        altura_janela = 600
        set_appearance_mode("dark")

        centralizar_janela(self, largura_janela, altura_janela)
        self.title("Minha Aplicação")
        self.resizable(False, False)
        self.iconbitmap("images/logoicon.ico")

        # Dicionário para guardar as páginas
        self.frames = {}

        # Instanciar todas as páginas e colocar no mesmo lugar
        for PageClass in (
            inicial, config, video_Assis, ajustes,
            termos_de_uso, modo_claro_escuro, idioma_software, comandos_coletanea
        ):
            page_name = PageClass.__name__
            frame = PageClass(self, self)
            self.frames[page_name] = frame
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.mostrar_pagina("modo_claro_escuro")

    def mostrar_pagina(self, nome):
        frame = self.frames[nome]
        frame.tkraise()

    def atualizar_tema(self):
        """Atualiza a cor de fundo de todas as páginas conforme o modo atual."""
        nova_cor = cor_atual()
        for frame in self.frames.values():
            frame.configure(fg_color=nova_cor)

if __name__ == "__main__": 
    app = App() 

    app.mainloop()