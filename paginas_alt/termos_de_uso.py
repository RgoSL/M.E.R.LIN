from customtkinter import *
from PIL import Image
from func_visual.widgets.header import nav

class termos_de_uso(CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        nav(self,controller, "M.E.R.LIN")

        Titulo = CTkLabel(
            self,
            text="Nossos Termos de Uso",
            font=("Arial", 20, "bold"),
            text_color=None,
            anchor="center",
            justify="center"
        )
        Titulo.place(relx=0.5, rely=0.2, anchor="center")

        quad = CTkScrollableFrame(self, fg_color="#654E82", corner_radius=15, border_width=2)
        quad.place(relx=0.5, rely=0.6, relwidth=0.85, relheight=0.6, anchor=CENTER)

        txt_termos = CTkLabel(quad, text="Termos de Uso", font=("Arial", 15, "bold"), text_color="#E6C8FA", wraplength=220)
        txt_termos.pack(pady = 10, padx = 5)

        txt_termos = CTkLabel(quad, 
                              text="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.", 
                              font=("Arial", 15, "bold"), text_color="#E6C8FA", wraplength=280)
        txt_termos.pack(pady = 10, padx = 5)

        icone_voltar = CTkImage(Image.open("assets/ImgsTemp/seta_esquerda.png"), size=(20, 20))

        # Botão de configurações
        btntst = CTkButton(
            self,
            image=icone_voltar,
            text="",
            fg_color="#654E82",
            command=lambda: self.controller.mostrar_pagina("ajustes")
        )

        btntst.place(relx=0.07, rely=0.15, anchor="center", relwidth=0.05, relheight=0.06)
