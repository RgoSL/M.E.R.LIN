from customtkinter import CTk
from paginas_alt.inicial import inicial
from paginas_alt.esc_config import config
from paginas_alt.video_assis import video_Assis
from paginas_alt.ajustes import ajustes
from paginas_alt.termos_de_uso import termos_de_uso
from paginas_alt.modo_claro_escuro import modo_claro_escuro
from paginas_alt.idioma_software import idioma_software

def centralizar_janela(janela, largura, altura):
    # Pega a largura e altura da tela do monitor
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()

    # Calcula a posição para centralizar
    x = int((largura_tela / 2) - (largura / 2))
    y = int((altura_tela / 2) - (altura / 2))

    # Define tamanho e posição
    janela.geometry(f"{largura}x{altura}+{x}+{y}")

class App(CTk):
    def __init__(self):
        super().__init__()
        largura_janela = 800
        altura_janela = 600

        centralizar_janela(self, largura_janela, altura_janela)
        self.title("Minha Aplicação")
        self.resizable(False, False)
        self.iconbitmap("images/logoicon.ico")
        # Dicionário para guardar as páginas
        self.frames = {}

        # Instanciar todas as páginas e colocar no mesmo lugar
        for PageClass in (inicial, config, video_Assis, ajustes,termos_de_uso,modo_claro_escuro, idioma_software):
            page_name = PageClass.__name__
            frame = PageClass(self, self)
            self.frames[page_name] = frame
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.mostrar_pagina("video_Assis")

    def mostrar_pagina(self, nome):
        frame = self.frames[nome]
        frame.tkraise()

if __name__ == "__main__":
    app = App()
    app.mainloop()