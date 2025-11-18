import os

from customtkinter import *
from func_visual.widgets.header import nav
from func_visual.widgets.progress import progress_bar
from PIL import Image, ImageDraw, ImageFont, ImageTk


class configSo(CTkFrame):
    def __init__(self, master, controller=None):
        super().__init__(master)
        self.controller = controller
        nav(self, controller, "M.E.R.LIN")

        self.label_msg_img = self.criar_texto_imagem(
            "Escolha a Base dos Seus Feitiços :", tamanho=30, cor="#000000"
        )
        self.label_msg = CTkLabel(self, image=self.label_msg_img, text="")
        self.label_msg.image = self.label_msg_img
        self.label_msg.place(relx=0.5, rely=0.2, anchor="center")

        # Container dos SOs
        self.Container_Sis = CTkFrame(self, fg_color="transparent")
        self.Container_Sis.place(relx=0.5, rely=0.5, anchor="center")

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
        self.grid_frame = CTkFrame(self.Container_Sis, fg_color="transparent")
        self.grid_frame.pack(padx=40, pady=20)

        # "Card" de Cada SO
        self.criar_card_so(
            self.grid_frame, self.img_windows, "Windows", 0, self.on_click_windows
        )
        self.criar_card_so(
            self.grid_frame, self.img_linux, "Linux", 1, self.on_click_linux
        )
        self.criar_card_so(self.grid_frame, self.img_mac, "macOS", 2, self.on_click_mac)

        # Barra de Progresso Temporária
        self.barra = progress_bar(
            self, cor_progresso="#C58ADE", modo="determinate", valor=0.3
        )
        self.barra.place(relx=0.5, rely=0.9, anchor="center")

        # Botões de Navegação
        self.btn_esquerdo = CTkButton(
            self,
            text="Voltar",
            text_color="#FFFFFF",
            fg_color="#654E82",
            font=("Gideon Roman", 20),
            bg_color="transparent",
            corner_radius=10,
            height=36,
            width=160,
            hover_color="#56397C",
            command=lambda: controller.mostrar_pagina("idioma_software"),
        )
        self.btn_esquerdo.place(relx=0.05, rely=0.9, anchor="w")

        self.btn_direito = CTkButton(
            self,
            text="Avançar",
            text_color="#FFFFFF",
            fg_color="#654E82",
            font=("Gideon Roman", 20),
            bg_color="transparent",
            corner_radius=10,
            height=36,
            width=160,
            hover_color="#56397C",
            command=lambda: controller.mostrar_pagina("config"),
        )
        self.btn_direito.place(relx=0.95, rely=0.9, anchor="e")

    def criar_texto_imagem(self, texto, tamanho=24, cor="#000000", padding=4):
        fonte_path = os.path.join("assets", "Fonts", "GideonRoman-Regular.ttf")
        fonte = ImageFont.truetype(fonte_path, tamanho)

        dummy_img = Image.new("RGBA", (1, 1))
        draw = ImageDraw.Draw(dummy_img)
        bbox = draw.textbbox((0, 0), texto, font=fonte)
        largura_texto = bbox[2] - bbox[0]
        altura_texto = bbox[3] - bbox[1]

        img = Image.new(
            "RGBA",
            (largura_texto + padding * 2, altura_texto + padding * 2),
            (0, 0, 0, 0),
        )
        draw = ImageDraw.Draw(img)
        draw.text((padding, padding), texto, font=fonte, fill=cor)

        return ImageTk.PhotoImage(img)

    # Função Para Padronizar as Imagens
    def ImgSis(self, src: str, tam: tuple = (100, 100)) -> CTkImage:
        img = Image.open(src)
        img_resized = img.resize(tam, Image.Resampling.LANCZOS)
        return CTkImage(light_image=img_resized, dark_image=img_resized, size=tam)

    # Função Para Padronizar a Criação dos "Cards"
    def criar_card_so(self, master, imagem, nome, coluna, comando):
        frame = CTkFrame(master, fg_color="transparent")
        frame.grid(row=0, column=coluna, padx=40, pady=10)

        # Botão que Torna a Imagem Clicável
        btn = CTkButton(
            frame,
            image=imagem,
            text="",
            width=150,
            height=150,
            fg_color="transparent",
            hover_color="#C58ADE",
            command=comando,
        )
        btn.pack()

        # Label que Fica Embaixo do Botão
        fonte_path = os.path.join("assets", "Fonts", "GowunDodum-Regular.ttf")
        label = CTkLabel(frame, text=nome, text_color="#000", font=(fonte_path, 14))
        label.pack(pady=5)

    # Funções Temporárias Para Testar os Botões
    def on_click_windows(self):
        print("Windows selecionado")

    def on_click_linux(self):
        print("Linux selecionado")

    def on_click_mac(self):
        print("MacOS selecionado")
