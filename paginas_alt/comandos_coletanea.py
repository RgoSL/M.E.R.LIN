from customtkinter import *
from PIL import Image
from func_visual.widgets.lista_comandos import criar_containers
from func_visual.widgets.header import nav
class comandos_coletanea(CTkFrame):
    def __init__(self,master,controller):
        super().__init__(master)
        self.controller = controller
        
        nav(self,controller, "M.E.R.LIN")

        titulo = CTkLabel(self, text="Comandos da Coletânea", font=("Bold", 20), text_color=None, bg_color="transparent")
        titulo.place(relx=0.5, rely=0.15, anchor=CENTER)

        quad = CTkScrollableFrame(self, fg_color="#654E82", corner_radius=15, bg_color="transparent", scrollbar_button_color="#F9B14F")
        quad.place(relx=0.5, rely=0.6, relwidth=0.8, relheight=0.6, anchor=CENTER)

        quad.selecao = StringVar(value="")

        criar_containers(quad,quad.selecao,cor_texto="black")

        icone_voltar = CTkImage(Image.open("assets/ImgsTemp/seta_esquerda.png"), size=(20, 20))

        # Botão de configurações
        btntst = CTkButton(
            self,
            image=icone_voltar,
            text="",
            fg_color="#654E82",
            command=lambda: self.controller.mostrar_pagina("inicial")
        )

        btntst.place(relx=0.07, rely=0.15, anchor="center", relwidth=0.05, relheight=0.06)