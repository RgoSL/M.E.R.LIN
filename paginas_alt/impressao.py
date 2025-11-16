from customtkinter import *
from PIL import Image
from func_visual.funcs_imgs.imagem import adicionar_imagem_texto
from func_visual.widgets.header import nav

class bemVindo(CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        nav(self, controller, "M.E.R.LIN")
        
        self.titulo = CTkLabel(
            self, text="Bem-Vindo(a) ao M.E.R.LIN", 
            font=("Bold", 30), 
            text_color="#654E82", 
            bg_color="transparent"
        )
        self.titulo.place(relx=0.5, rely=0.2, anchor="center")

        self.imagem = adicionar_imagem_texto(
            self, 
            caminho_img="assets/ImgsTemp/placeholder.jpg", 
            texto="Configurando o Poder", 
            cor="transparent",
            tamanho=230, 
            espacamento=30,  
            cor_texto=None
        )
        self.imagem.place(relx=0.5, rely=0.55, anchor="center")

        self.btn_iniciar = CTkButton(
            self, 
            text="Iniciar", 
            font=("Bold", 20), 
            height=36, 
            width=160,  
            text_color="#FFFFFF", 
            bg_color="transparent", 
            fg_color="#654E82", 
            corner_radius=10,  
            hover_color="#56397C",
            command=lambda: controller.mostrar_pagina("idioma_software")  
        )
        self.btn_iniciar.place(relx=0.5, rely=0.9, anchor="center")