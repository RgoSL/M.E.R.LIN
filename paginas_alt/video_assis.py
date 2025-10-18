from customtkinter import *
from PIL import Image
import os
from func_visual.widgets.header import nav

class video_Assis(CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        nav(self,controller, "M.E.R.LIN")

        titulo = CTkLabel(self, text="Assistente de Vídeo", font=("Bold", 20), text_color="black", bg_color="transparent")
        titulo.place(relx=0.5, rely=0.15, anchor=CENTER)

        quad = CTkScrollableFrame(self, fg_color="#654E82", corner_radius=15, bg_color="transparent",orientation="horizontal", scrollbar_button_color="#F9B14F")
        quad.place(relx=0.5, rely=0.6, relwidth=0.8, relheight=0.6, anchor=CENTER)

        sub_titulo = CTkLabel(quad, text="Selecione o vídeo:", font=("Bold", 18), text_color="black")
        sub_titulo.pack(pady=10, padx=240)

        frame = CTkFrame(quad, fg_color="white", corner_radius=15, border_color="#C58ADE", border_width=2)
        frame.place(relx=0.5, rely=0.5, relwidth=0.8, relheight=0.6, anchor=CENTER)

        icone_voltar = CTkImage(Image.open("assets/ImgsTemp/seta_esquerda.png"), size=(20, 20))

        # Botão de configurações
        btntst = CTkButton(
            self,
            image=icone_voltar,
            text="",
            fg_color="#654E82",
            command=lambda: self.controller.mostrar_pagina("config")
        )

        btntst.place(relx=0.07, rely=0.15, anchor="center", relwidth=0.05, relheight=0.06)
    
        