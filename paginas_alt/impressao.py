from customtkinter import *
from func_visual.funcs_imgs.imagem import adicionar_imagem_texto
from func_visual.widgets.header import nav
from func_visual.widgets.i18n import i18n
from PIL import Image, ImageDraw, ImageFont, ImageTk

class bemVindo(CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        nav(self, controller, "M.E.R.LIN")

        self.titulo = CTkLabel(self, text="", bg_color="transparent")
        self.titulo.place(relx=0.8, rely=0.25, anchor="center")

        self.imagem = None
        self.criar_imagem_central()

        self.btn_iniciar = CTkButton(
            self,
            text=i18n.t("iniciar"),
            font=("Gideon Roman", 20, "bold"),
            height=36,
            width=160,
            text_color="#FFFFFF",
            bg_color="transparent",
            fg_color="#654E82",
            corner_radius=10,
            hover_color="#56397C",
            command=lambda: controller.mostrar_pagina("idioma_software"),
        )
        self.btn_iniciar.place(relx=0.5, rely=0.9, anchor="center")

        self.criar_titulo()

    def criar_titulo(self):
        texto = i18n.t("titulo_impressao")
        
        img = Image.new("RGBA", (1000, 140), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        fonte_personalizada = ImageFont.truetype(
            "assets/fonts/GideonRoman-Regular.ttf", 40
        )
        draw.text((10, 10), texto, font=fonte_personalizada, fill="#654E82")

        img_titulo_tk = ImageTk.PhotoImage(img)
        self.titulo.configure(image=img_titulo_tk)
        self.titulo.image = img_titulo_tk  

    def criar_imagem_central(self):
        if self.imagem:
            self.imagem.destroy()

        self.imagem = adicionar_imagem_texto(
            self,
            caminho_img_dark="assets/ImgsConfig/BemVindoImg.png",
            texto=i18n.t("subtitulo_impressao"),
            cor="transparent",
            tamanho=230,
            espacamento=30,
            cor_texto="#654E82"
        )
        self.imagem.place(relx=0.5, rely=0.55, anchor="center")

    def atualizar_idioma(self):
        self.criar_titulo()
        
        self.criar_imagem_central()

        self.btn_iniciar.configure(text=i18n.t("iniciar"))
        
        print(f"✓ Página bemVindo atualizada para idioma: {i18n.idioma_atual}")