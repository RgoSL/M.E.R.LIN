import os
import tkinter.font as tkfont

from customtkinter import *
from func_visual.funcs_imgs.imagem import adicionar_imagem_texto
from func_visual.modos.ui_mode import alternar_modo
from func_visual.widgets.header import nav
from func_visual.widgets.progress import progress_bar
from func_visual.widgets.i18n import i18n
from PIL import Image, ImageDraw, ImageFont, ImageTk

class modo_claro_escuro(CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        try:
            self.debug_fonts()
        except Exception as e:
            print("Erro ao achar a fonte:", e)

        nav(self, controller, "M.E.R.LIN")

        self.titulo_label = CTkLabel(self, text="", anchor="center")
        self.titulo_label.place(relx=0.5, rely=0.2, anchor="center")

        self.label_claro = None
        self.label_escuro = None

        self.btn_claro = adicionar_imagem_texto(
            self,
            caminho_img_dark="assets/ImgsConfig/temaClaroEscuro.png",
            caminho_img_light="assets/ImgsConfig/TemaClaroImg.png",
            cor="transparent",
            tamanho=150,
            espacamento=20,
            texto=i18n.t("tema_claro"),
            cor_texto="#654E82",
            comando=self.trocar_modo,
        )
        self.btn_claro.place(relx=0.2, rely=0.5, anchor=CENTER)

        self.btn_escuro = adicionar_imagem_texto(
            self,
            caminho_img_dark="assets/ImgsConfig/temaEscuroEscuro.png",
            caminho_img_light="assets/ImgsConfig/TemaEscuroImg.png",
            cor="transparent",
            tamanho=150,
            espacamento=20,
            texto=i18n.t("tema_escuro"),
            cor_texto="#654E82",
            comando=self.trocar_modo,
        )
        self.btn_escuro.place(relx=0.8, rely=0.5, anchor=CENTER)

        self.barra = progress_bar(
            self, cor_progresso="#C58ADE", modo="determinate", valor=0.8
        )
        self.barra.place(relx=0.5, rely=0.9, anchor=CENTER)

        self.btn_voltar = CTkButton(
            self,
            text=i18n.t("voltar"),
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
        self.btn_voltar.place(relx=0.05, rely=0.9, anchor="w")

        self.btn_avancar = CTkButton(
            self,
            text=i18n.t("avancar"),
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
        self.btn_avancar.place(relx=0.95, rely=0.9, anchor="e")

        self.criar_titulo_imagem()

    def criar_titulo_imagem(self):
        texto = i18n.t("titulo_temas")
        
        fonte_path = os.path.join("assets", "Fonts", "GideonRoman-Regular.ttf")
        img = Image.new("RGBA", (700, 120), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        fonte_gideon = ImageFont.truetype(fonte_path, 30)

        bbox = draw.textbbox((0, 0), texto, font=fonte_gideon)
        texto_largura = bbox[2] - bbox[0]
        texto_altura = bbox[3] - bbox[1]
        pos_x = (700 - texto_largura) // 2
        pos_y = (120 - texto_altura) // 2
        
        draw.text((pos_x, pos_y), texto, font=fonte_gideon, fill="#654E82")

        img_tk = ImageTk.PhotoImage(img)
        self.titulo_label.configure(image=img_tk)
        self.titulo_label.image = img_tk 

    def atualizar_idioma(self):

        self.criar_titulo_imagem()
        
        self.btn_voltar.configure(text=i18n.t("voltar"))
        self.btn_avancar.configure(text=i18n.t("avancar"))
        
        
        print(f"Página modo_claro_escuro atualizada para idioma: {i18n.idioma_atual}")

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