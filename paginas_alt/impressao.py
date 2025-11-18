from customtkinter import *
from func_visual.funcs_imgs.imagem import adicionar_imagem_texto
from func_visual.widgets.header import nav
from PIL import Image, ImageDraw, ImageFont, ImageTk


class bemVindo(CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        nav(self, controller, "M.E.R.LIN")

        img = Image.new("RGBA", (1000, 140), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        fonte_personalizada = ImageFont.truetype(
            "assets/fonts/GideonRoman-Regular.ttf", 40
        )

        texto_titulo = "Bem-Vindo(a) ao M.E.R.LIN"

        draw.text((10, 10), texto_titulo, font=fonte_personalizada, fill="#654E82")

        self.img_titulo_tk = ImageTk.PhotoImage(img)

        self.titulo = CTkLabel(
            self, image=self.img_titulo_tk, text="", bg_color="transparent"
        )
        self.titulo.place(relx=0.8, rely=0.25, anchor="center")

        self.imagem = adicionar_imagem_texto(
            self,
            caminho_img="assets/ImgsTemp/placeholder.jpg",
            texto="Configurando o Poder",
            cor="transparent",
            tamanho=230,
            espacamento=30,
            cor_texto=None,
        )
        self.imagem.place(relx=0.5, rely=0.55, anchor="center")

        self.btn_iniciar = CTkButton(
            self,
            text="Iniciar",
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
