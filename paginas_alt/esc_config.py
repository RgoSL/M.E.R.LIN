import os

from customtkinter import *
from func_visual.funcs_imgs.imagem import adicionar_imagem_texto
from func_visual.widgets.header import nav
from func_visual.widgets.progress import progress_bar
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

        img_title = Image.new("RGBA", (900, 120), (0, 0, 0, 0))
        draw_title = ImageDraw.Draw(img_title)

        fonte_titulo = ImageFont.truetype("assets/fonts/GideonRoman-Regular.ttf", 30)

        texto_titulo = "Escolha Como se Preparar"

        draw_title.text((10, 10), texto_titulo, font=fonte_titulo, fill="#654E82")

        self.img_title_tk = ImageTk.PhotoImage(img_title)

        self.label = CTkLabel(
            self, image=self.img_title_tk, text="", bg_color="transparent"
        )
        self.label.place(relx=0.83, rely=0.23, anchor=CENTER)

        img_sub = Image.new("RGBA", (700, 80), (0, 0, 0, 0))
        draw_sub = ImageDraw.Draw(img_sub)

        fonte_sub = ImageFont.truetype("assets/fonts/GideonRoman-Regular.ttf", 17)

        texto_sub = "Tipo de Configuração:"

        draw_sub.text((10, 5), texto_sub, font=fonte_sub, fill="#654E82")

        self.img_sub_tk = ImageTk.PhotoImage(img_sub)

        self.Label2 = CTkLabel(
            self, image=self.img_sub_tk, text="", bg_color="transparent"
        )
        self.Label2.place(relx=0.93, rely=0.38, anchor=CENTER)

        radio_var = IntVar()


        def avanc():
            escolha = radio_var.get()

            if escolha == 1:
                self.closeOpenDock()

            elif escolha == 2:
                self.controller.mostrar_pagina("ajustes")

            else:
                from CTkMessagebox import CTkMessagebox

                CTkMessagebox(
                    title="Atenção!",
                    message="Por favor, escolha uma das opções",
                    icon="warning",
                    option_1="OK",
                    fade_in_duration=50,
                    fg_color="#654E82",
                    bg_color="#654E82",
                    button_color="#F9B14F",
                )
        
        frame_check = CTkFrame(
            self,
            fg_color="white",
            corner_radius=15,
            border_color="#C58ADE",
            border_width=2,
            bg_color="transparent",
        )
        frame_check.place(
            relx=0.7, rely=0.45, relwidth=0.4, relheight=0.13, anchor=CENTER
        )

        radio1 = CTkRadioButton(
            frame_check,
            text="Rápida",
            font=("Bold", 15),
            text_color="black",
            variable=radio_var,
            value=1,
            fg_color="#654E82",
        )
        radio1.place(relx=0.2, rely=0.5, anchor=CENTER)

        frame_check2 = CTkFrame(
            self,
            fg_color="white",
            corner_radius=15,
            border_color="#C58ADE",
            border_width=2,
            bg_color="transparent",
        )
        frame_check2.place(
            relx=0.7, rely=0.6, relwidth=0.4, relheight=0.13, anchor=CENTER
        )

        radio2 = CTkRadioButton(
            frame_check2,
            text="Personalizada",
            font=("Bold", 15),
            text_color="black",
            variable=radio_var,
            value=2,
            fg_color="#654E82",
        )
        radio2.place(relx=0.23, rely=0.5, anchor=CENTER)

        btn_voltar = CTkButton(
            self,
            text="Voltar",
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

        btn_proximo = CTkButton(
            self,
            text="Avançar",
            font=("Gideon Roman", 20),
            text_color="#FFFFFF",
            bg_color="transparent",
            height=40,
            width=60,
            fg_color="#654E82",
            corner_radius=10,
            hover_color="#56397C",
            command=avanc,
        )

        btn_voltar.place(
            relx=0.15, rely=0.9, anchor=CENTER, relwidth=0.2, relheight=0.06
        )
        btn_proximo.place(
            relx=0.85, rely=0.9, anchor=CENTER, relwidth=0.2, relheight=0.06
        )

        self.barra = progress_bar(
            self, cor_progresso="#C58ADE", modo="determinate", valor=0.5
        )
        self.barra.place(relx=0.5, rely=0.9, anchor=CENTER)
    def closeOpenDock(self):
        self.controller.withdraw()

        from paginas_alt.dock import Dock

        Dock(self.controller, self.controller)