import os

from customtkinter import *
from func_visual.funcs_imgs.imagem import adicionar_imagem_texto
from func_visual.widgets.header import nav
from func_visual.widgets.progress import progress_bar
from func_visual.widgets.i18n import i18n
from PIL import Image, ImageDraw, ImageFont, ImageTk

class config(CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        logo = adicionar_imagem_texto(
            self,
            caminho_img_dark="assets/ImgsConfig/ModoEscuroConfigImg.png",
            caminho_img_light="assets/ImgsConfig/ModoConfigImg.png",
            texto="",
            cor="transparent",
            tamanho=160,
            espacamento=10,
            cor_texto=None,
        )
        logo.place(relx=0.2, rely=0.5, anchor=CENTER)

        nav(self, controller, "M.E.R.LIN")

        self.label_titulo = CTkLabel(self, text="", bg_color="transparent")
        self.label_titulo.place(relx=0.83, rely=0.23, anchor=CENTER)

        self.label_subtitulo = CTkLabel(self, text="", bg_color="transparent")
        self.label_subtitulo.place(relx=0.93, rely=0.38, anchor=CENTER)

        self.radio_var = IntVar()

        self.frame_check = CTkFrame(
            self,
            fg_color="white",
            corner_radius=15,
            border_color="#C58ADE",
            border_width=2,
            bg_color="transparent",
        )
        self.frame_check.place(
            relx=0.7, rely=0.45, relwidth=0.4, relheight=0.13, anchor=CENTER
        )

        self.radio1 = CTkRadioButton(
            self.frame_check,
            text=i18n.t("config_rpd"),
            font=("Bold", 15),
            text_color="black",
            variable=self.radio_var,
            value=1,
            fg_color="#654E82",
        )
        self.radio1.place(relx=0.2, rely=0.5, anchor=CENTER)

        self.frame_check2 = CTkFrame(
            self,
            fg_color="white",
            corner_radius=15,
            border_color="#C58ADE",
            border_width=2,
            bg_color="transparent",
        )
        self.frame_check2.place(
            relx=0.7, rely=0.6, relwidth=0.4, relheight=0.13, anchor=CENTER
        )

        self.radio2 = CTkRadioButton(
            self.frame_check2,
            text=i18n.t("config_per"),
            font=("Bold", 15),
            text_color="black",
            variable=self.radio_var,
            value=2,
            fg_color="#654E82",
        )
        self.radio2.place(relx=0.23, rely=0.5, anchor=CENTER)

        self.btn_voltar = CTkButton(
            self,
            text=i18n.t("voltar"),
            font=("Gideon Roman", 20),
            text_color="#FFFFFF",
            bg_color="transparent",
            height=40,
            width=60,
            fg_color="#654E82",
            corner_radius=10,
            hover_color="#56397C",
            command=lambda: controller.mostrar_pagina("configSo"),
        )
        self.btn_voltar.place(
            relx=0.15, rely=0.9, anchor=CENTER, relwidth=0.2, relheight=0.06
        )

        self.btn_proximo = CTkButton(
            self,
            text=i18n.t("avancar"),
            font=("Gideon Roman", 20),
            text_color="#FFFFFF",
            bg_color="transparent",
            height=40,
            width=60,
            fg_color="#654E82",
            corner_radius=10,
            hover_color="#56397C",
            command=self.avancar,
        )
        self.btn_proximo.place(
            relx=0.85, rely=0.9, anchor=CENTER, relwidth=0.2, relheight=0.06
        )

        self.barra = progress_bar(
            self, cor_progresso="#C58ADE", modo="determinate", valor=0.5
        )
        self.barra.place(relx=0.5, rely=0.9, anchor=CENTER)

        self.criar_titulo()
        self.criar_subtitulo()

    def criar_titulo(self):
        texto = i18n.t("titulo_config")
        
        img_title = Image.new("RGBA", (900, 120), (0, 0, 0, 0))
        draw_title = ImageDraw.Draw(img_title)
        fonte_titulo = ImageFont.truetype("assets/fonts/GideonRoman-Regular.ttf", 30)
        draw_title.text((10, 10), texto, font=fonte_titulo, fill="#654E82")

        img_title_tk = ImageTk.PhotoImage(img_title)
        self.label_titulo.configure(image=img_title_tk)
        self.label_titulo.image = img_title_tk

    def criar_subtitulo(self):
        texto = i18n.t("subtitulo_config")
        
        img_sub = Image.new("RGBA", (700, 80), (0, 0, 0, 0))
        draw_sub = ImageDraw.Draw(img_sub)
        fonte_sub = ImageFont.truetype("assets/fonts/GideonRoman-Regular.ttf", 17)
        draw_sub.text((10, 5), texto, font=fonte_sub, fill="#654E82")

        img_sub_tk = ImageTk.PhotoImage(img_sub)
        self.label_subtitulo.configure(image=img_sub_tk)
        self.label_subtitulo.image = img_sub_tk  

    def atualizar_idioma(self):

        self.criar_titulo()
        self.criar_subtitulo()
        
        self.radio1.configure(text=i18n.t("config_rpd"))
        self.radio2.configure(text=i18n.t("config_per"))
        
        self.btn_voltar.configure(text=i18n.t("voltar"))
        self.btn_proximo.configure(text=i18n.t("avancar"))
        
        print(f"✓ Página config atualizada para idioma: {i18n.idioma_atual}")

    def avancar(self):
        escolha = self.radio_var.get()

        if escolha == 1:
            self.closeOpenDock()

        elif escolha == 2:
            self.controller.mostrar_pagina("ajustes")

        else:
            from CTkMessagebox import CTkMessagebox

            CTkMessagebox(
                title=i18n.t("alerta"),
                message=i18n.t("mensagem_alerta"),
                icon="warning",
                option_1="OK",
                fade_in_duration=50,
                fg_color="#654E82",
                bg_color="#654E82",
                button_color="#F9B14F",
                button_hover_color= "#ECA541" ,
            )

    def closeOpenDock(self):
        self.controller.withdraw()

        from paginas_alt.dock import Dock

        Dock(self.controller, self.controller)