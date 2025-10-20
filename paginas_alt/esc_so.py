# Bibliotecas Utilizadas 
from customtkinter import *
from PIL import Image
from func_visual.widgets.progress import progress_bar
import os
# Import da Barra de Progresso Padrão do Software


# Função de Criação da Classe Dessa Tela
class configSo(CTkFrame):
    def __init__(self, master, controller=None):
        super().__init__(master)
        self.controller = controller
        
        # Mensagem da Página        
        self.label_msg = CTkLabel(
        self, text = "Selecione seu Sistema Operacional", text_color = "#000000", font = ("arial", 20, "bold"))
        self.label_msg.place(relx = 0.5, rely = 0.2, anchor = "center")

        # Container dos SOs
        self.Container_Sis = CTkFrame(
        self, fg_color = "#FFFFFF", border_color = "#C58ADE", border_width = 2)
        self.Container_Sis.place(relx = 0.5, rely = 0.5, anchor = "center") 

        BASE_DIR = os.path.dirname(os.path.dirname(__file__))

        # Caminho de Cada Imagem de Sistema
        caminho_win = os.path.join(BASE_DIR, "assets", "ImgsSo", "IconWin.png")
        caminho_lin = os.path.join(BASE_DIR, "assets", "ImgsSo", "IconLin.png")
        caminho_mac = os.path.join(BASE_DIR, "assets", "ImgsSo", "IconMac.png")

        # Padronização das Imagens
        tamanho_icones = (150, 150)

        # Exibir as Imagens
        self.img_windows = self.ImgSis(caminho_win, tamanho_icones)
        self.img_linux = self.ImgSis(caminho_lin, tamanho_icones)
        self.img_mac = self.ImgSis(caminho_mac, tamanho_icones)

        # Padronização dos "Cards"
        self.grid_frame = CTkFrame(self.Container_Sis, fg_color = "transparent")
        self.grid_frame.pack(padx = 40, pady = 20)

        # "Card" de Cada SO
        self.criar_card_so(self.grid_frame, self.img_windows, "Windows", 0, self.on_click_windows)
        self.criar_card_so(self.grid_frame, self.img_linux, "Linux", 1, self.on_click_linux)
        self.criar_card_so(self.grid_frame, self.img_mac, "macOS", 2, self.on_click_mac)

        # Barra de Progresso Temporária
        self.barra = progress_bar(self, cor_progresso="#C58ADE", modo="determinate", valor=0.5)
        self.barra.place(relx=0.5, rely=0.9, anchor="center")

        # Botões de Navegação
        self.btn_esquerdo = CTkButton(self, text = "Voltar", text_color = "#FFFFFF", fg_color = "#654E82", bg_color = "transparent", corner_radius = 10,  height= 33, width= 103, hover_color = "#56397C",command=lambda: controller.mostrar_pagina("modo_claro_escuro"))
        self.btn_esquerdo.place(relx=0.05, rely=0.9, anchor="w")

        self.btn_direito = CTkButton(self, text = "Próximo", text_color = "#FFFFFF", fg_color = "#654E82", bg_color = "transparent", corner_radius = 10, height= 33, width= 103, hover_color = "#56397C", command=lambda: controller.mostrar_pagina("idioma_software")) 
        self.btn_direito.place(relx=0.95, rely=0.9, anchor="e")

        self.barra = progress_bar(self, cor_progresso="#C58ADE", modo="determinate", valor=0.5)
        self.barra.place(relx=0.5, rely=0.9, anchor="center")


    # Função Para Padronizar as Imagens
    def ImgSis(self, src: str, tam: tuple = (100, 100)) -> CTkImage:
        img = Image.open(src)
        img_resized = img.resize(tam, Image.Resampling.LANCZOS)
        return CTkImage(light_image = img_resized, dark_image = img_resized, size = tam)

    # Função Para Padronizar a Criação dos "Cards"
    def criar_card_so(self, master, imagem, nome, coluna, comando):
        frame = CTkFrame(master, fg_color="transparent")
        frame.grid(row = 0, column = coluna, padx = 40, pady = 10)

        # Botão que Torna a Imagem Clicável
        btn = CTkButton(
    frame, image = imagem, text = "", width = 150, height = 150, fg_color = "transparent", hover_color = "#EEE0F4", command = comando)
        btn.pack()

        # Label que Fica Embaixo do Botão
        label = CTkLabel(frame, text = nome, text_color = "#000000", font =("arial", 14, "bold"))
        label.pack(pady=5)

    # Funções Temporárias Para Testar os Botões
    def on_click_windows(self):
        print("Windows selecionado")

    def on_click_linux(self):
        print("Linux selecionado")

    def on_click_mac(self):
        print("MacOS selecionado")

    def voltar(self):
        print("Voltando...")

    def avancar(self):
        print("Avançando...")

# Execução Local e Temporária Dessa Classe
if __name__ == "__main__":
    set_appearance_mode("dark")
    set_default_color_theme("blue")

    app = CTk()
    app.geometry("900x600")
    app.title("Tela de Configuração de Sistema")

    tela_config = configSo(master=app)
    tela_config.pack(fill="both", expand=True)

    app.mainloop()