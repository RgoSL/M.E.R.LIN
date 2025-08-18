from customtkinter import *
from PIL import Image

class termos_de_uso(CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        self.configure(fg_color="#FFFFFF")

        header = CTkFrame(self, fg_color="#654E82", corner_radius=0)
        header.place(relx=0, rely=0, relwidth=1, relheight=0.1)

        txt_logo = CTkLabel(header, text="M.E.R.LIN", font=("Bold", 20), text_color="#E6C8FA")
        txt_logo.place(relx=0.1, rely=0.5, anchor=CENTER)

        Titulo = CTkLabel(
            self,
            text="Nossos Termos de Uso",
            font=("Arial", 20, "bold"),
            text_color="black",
            anchor="center",
            justify="center"
        )
        Titulo.place(relx=0.5, rely=0.2, anchor="center")

        quad = CTkScrollableFrame(self, fg_color="#654E82", corner_radius=15, border_width=2)
        quad.place(relx=0.5, rely=0.6, relwidth=0.8, relheight=0.6, anchor=CENTER)

        txt_termos = CTkLabel(quad, text="Termos de Uso", font=("Arial", 15, "bold"), text_color="black", wraplength=220)
        txt_termos.pack(pady = 10, padx = 5)

        txt_termos = CTkLabel(quad, 
                              text="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.", 
                              font=("Arial", 15, "bold"), text_color="#E6C8FA", wraplength=280)
        txt_termos.pack(pady = 10, padx = 5)

        icone_voltar = CTkImage(Image.open("images/seta_esquerda.png"), size=(20, 20))

        # Botão de configurações
        btntst = CTkButton(
            self,
            image=icone_voltar,
            text="",
            fg_color="#654E82",
            command=lambda: self.controller.mostrar_pagina("config")
        )

        btntst.place(relx=0.07, rely=0.15, anchor="center", relwidth=0.05, relheight=0.06)
