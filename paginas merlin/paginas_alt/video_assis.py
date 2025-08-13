from customtkinter import *
from PIL import Image
import os


class video_Assis(CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        frame = CTkFrame(self, fg_color="#FFFFFF", corner_radius=0)
        frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        header = CTkFrame(self, fg_color="#654E82", corner_radius=0)
        header.place(relx=0, rely=0, relwidth=1, relheight=0.1)

        txt_logo = CTkLabel(header, text="M.E.R.LIN", font=("Bold", 20), text_color="#E6C8FA")
        txt_logo.place(relx=0.1, rely=0.5, anchor=CENTER)

        titulo = CTkLabel(header, text="Assistente de Vídeo", font=("Bold", 20), text_color="black")
        titulo.place(relx=0.5, rely=0.5, anchor=CENTER)

        quad = CTkScrollableFrame(self, fg_color="#654E82", corner_radius=15, bg_color="white",orientation="horizontal", scrollbar_button_color="#F9B14F")
        quad.place(relx=0.5, rely=0.6, relwidth=0.8, relheight=0.6, anchor=CENTER)

        sub_titulo = CTkLabel(quad, text="Selecione o vídeo:", font=("Bold", 18), text_color="black")
        sub_titulo.pack(pady=10, padx=240)

        frame = CTkFrame(quad, fg_color="white", corner_radius=15, border_color="#C58ADE", border_width=2)
        frame.place(relx=0.5, rely=0.5, relwidth=0.8, relheight=0.6, anchor=CENTER)

        btn = CTkButton(self, text="Próximo", font=("Bold", 15), text_color="black", fg_color="#F9B14F", command=lambda: controller.mostrar_pagina("inicial"))
        btn.place(relx=0.93, rely=0.15, anchor=CENTER,relwidth=0.09)

        