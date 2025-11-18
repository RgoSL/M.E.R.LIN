import ctypes

from customtkinter import *

from paginas_alt.ajustes import ajustes
from paginas_alt.comandos_coletanea import comandos_coletanea
from paginas_alt.esc_config import config
from paginas_alt.esc_so import configSo
from paginas_alt.idioma_software import idioma_software
from paginas_alt.impressao import bemVindo
from paginas_alt.inicial import inicial
from paginas_alt.modo_claro_escuro import modo_claro_escuro
from paginas_alt.termos_de_uso import termos_de_uso
from paginas_alt.video_assis import video_Assis


def centralizar_janela(janela, largura, altura):
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()
    x = int((largura_tela / 2) - (largura / 2))
    y = int((altura_tela / 2) - (altura / 2))
    janela.geometry(f"{largura}x{altura}+{x}+{y}")


def cor_atual():

    modo = get_appearance_mode()
    return "#FFFFFF" if modo == "Light" else "#2B2B2B"


class App(CTk):
    def __init__(self):
        super().__init__()

        set_appearance_mode("dark")
        self.largura_janela = 800
        self.altura_janela = 600
        self.radius = 30
        centralizar_janela(self, self.largura_janela, self.altura_janela)
        self.configure(fg_color="#2B2B2B")
        self.overrideredirect(True)
        self.app_selecionado = None
        self.after(100, self.arredondar_janela)

        self.main_frame = CTkFrame(self, fg_color="#2B2B2B", corner_radius=self.radius)
        self.main_frame.pack(expand=True, fill="both")

        self.title_bar = CTkFrame(self.main_frame, height=30, fg_color="#1E1E1E")
        self.title_bar.pack(fill="x", side="top")

        self.title_label = CTkLabel(
            self.title_bar, text="Minha Aplicação", fg_color="#1E1E1E"
        )
        self.title_label.pack(side="left", padx=10)

        self.frames = {}
        pages = [
            bemVindo,
            idioma_software,
            configSo,
            config,
            modo_claro_escuro,
            ajustes,
            inicial,
            termos_de_uso,
        ]
        for PageClass in pages:
            page_name = PageClass.__name__
            try:
                frame = PageClass(self.main_frame, self)
                self.frames[page_name] = frame
                frame.place(relx=0, rely=0, relwidth=1, relheight=1)
            except Exception as e:
                print(f"Erro ao inicializar página {page_name}: {e}")

        self.mostrar_pagina(pages[0].__name__)
        self.maximized = False

    def arredondar_janela(self):
        try:
            hwnd = ctypes.windll.user32.GetParent(self.winfo_id())
            region = ctypes.windll.gdi32.CreateRoundRectRgn(
                0,
                0,
                self.largura_janela + 1,
                self.altura_janela + 1,
                self.radius,
                self.radius,
            )
            ctypes.windll.user32.SetWindowRgn(hwnd, region, True)
        except Exception as e:
            print("Erro ao arredondar a janela:", e)

    def mostrar_pagina(self, nome):
        if nome in self.frames:
            self.frames[nome].tkraise()

    def atualizar_tema(self):
        modo = get_appearance_mode()
        if modo == "Light":
            nova_cor = "#FFFFFF"
        else:
            nova_cor = "#2B2B2B"

        for frame in self.frames.values():
            frame.configure(fg_color=nova_cor)

        self.main_frame.configure(fg_color=nova_cor)
        self.title_bar.configure(fg_color="#1E1E1E")

    def aplicar_tema_personalizado(self):
        modo = get_appearance_mode()

        if modo == "Light":
            bg_cor = "#FFFFFF"
            texto_cor = "#000000"
        else:
            bg_cor = "#2B2B2B"
            texto_cor = "#FFFFFF"

        self.configure(fg_color=bg_cor)
        self.main_frame.configure(fg_color=bg_cor)

        for frame in self.frames.values():
            frame.configure(fg_color=bg_cor)
            for widget in frame.winfo_children():
                try:
                    widget.configure(fg_color=bg_cor, text_color=texto_cor)
                except:
                    pass


if __name__ == "__main__":
    app = App()
    app.mainloop()
