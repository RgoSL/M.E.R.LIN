import os
import tkinter.font as tkfont

from customtkinter import *
from func_visual.funcs_imgs.imagem import adicionar_imagem_texto
from func_visual.modos.ui_mode import alternar_modo
from func_visual.widgets.header import nav
from func_visual.widgets.progress import progress_bar
from PIL import Image, ImageDraw, ImageFont, ImageTk


class modo_claro_escuro(CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        try:
            self.debug_fonts()
        except Exception as e:
            print("⚠️ Erro ao achar a fonte:", e)

        nav(self, controller, "M.E.R.LIN")

        self.titulo_label = self.criar_titulo_imagem(
            texto="Estilo é Poder. Qual o Seu?",
            tamanho=30,
            cor="#654E82",
            largura=700,
            altura=120,
        )
        self.titulo_label.place(relx=0.5, rely=0.2, anchor="center")

        claro = adicionar_imagem_texto(
            self,
            caminho_img_dark="assets/ImgsConfig/temaClaroEscuro.png",
            caminho_img_light="assets/ImgsConfig/TemaClaroImg.png",
            cor="transparent",
            tamanho=150,
            espacamento=20,
            texto="Tema Claro",
            cor_texto="#654E82",
            comando=self.trocar_modo,
        )
        claro.place(relx=0.2, rely=0.5, anchor=CENTER)

        escuro = adicionar_imagem_texto(
            self,
            caminho_img_dark="assets/ImgsConfig/temaEscuroEscuro.png",
            caminho_img_light="assets/ImgsConfig/TemaEscuroImg.png",
            cor="transparent",
            tamanho=150,
            espacamento=20,
            texto="Tema Escuro",
            cor_texto="#654E82",
            comando=self.trocar_modo,
        )
        escuro.place(relx=0.8, rely=0.5, anchor=CENTER)

        # Barra de progresso
        self.barra = progress_bar(
            self, cor_progresso="#C58ADE", modo="determinate", valor=0.8
        )
        self.barra.place(relx=0.5, rely=0.9, anchor=CENTER)

        btn_voltar = CTkButton(
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
            command=lambda: self.controller.mostrar_pagina("config"),
        )
        btn_voltar.place(relx=0.05, rely=0.9, anchor="w")

        btn_avancar = CTkButton(
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
            command=lambda: self.controller.mostrar_pagina("ajustes"),
        )
        btn_avancar.place(relx=0.95, rely=0.9, anchor="e")

    def criar_titulo_imagem(self, texto, tamanho, cor, largura, altura):
        fonte_path = os.path.join("assets", "Fonts", "GideonRoman-Regular.ttf")

        img = Image.new("RGBA", (largura, altura), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        fonte_gideon = ImageFont.truetype(fonte_path, tamanho)

        bbox = draw.textbbox((0, 0), texto, font=fonte_gideon)
        texto_largura = bbox[2] - bbox[0]
        texto_altura = bbox[3] - bbox[1]
        pos_x = (largura - texto_largura) // 2
        pos_y = (altura - texto_altura) // 2
        draw.text((pos_x, pos_y), texto, font=fonte_gideon, fill=cor)

        img_tk = ImageTk.PhotoImage(img)

        label_img = CTkLabel(self, image=img_tk, text="")
        label_img.image = img_tk

        return label_img

    def debug_fonts(self):
        font_src = os.path.join("assets", "Fonts")
        Gideon = os.path.join(font_src, "GideonRoman-Regular.ttf")
        Gowun = os.path.join(font_src, "GowunDodum-Regular.ttf")

        self.tk.call(
            "font", "create", "GideonRoman", "-family", "GideonRoman", "-size", 12
        )
        self.tk.call(
            "font", "create", "GowunDodum", "-family", "GowunDodum", "-size", 12
        )

    def trocar_modo(self):
        alternar_modo()

        modo_atual = get_appearance_mode()
        self.cor_fundo = "#FFFFFF" if modo_atual == "Light" else "#2B2B2B"
        self.configure(fg_color=self.cor_fundo)

        self.controller.atualizar_tema()
