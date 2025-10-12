from customtkinter import *
from PIL import Image
from func_visual.funcs_imgs.imagem import adicionar_imagem_texto
from func_visual.widgets.progress import progress_bar
from func_visual.modos.ui_mode import alternar_modo  # função que alterna claro/escuro

class modo_claro_escuro(CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        # Cabeçalho
        header = CTkFrame(self, fg_color="#654E82", corner_radius=0)
        header.place(relx=0, rely=0, relwidth=1, relheight=0.1)
        txt_logo = CTkLabel(header, text="M.E.R.LIN", font=("Bold", 20), text_color="#E6C8FA")
        txt_logo.place(relx=0.1, rely=0.5, anchor=CENTER)

        # Título
        titulo = CTkLabel(
            self,
            text="Modo Claro e Escuro",
            font=("Arial", 20, "bold"),
            text_color=None,
            anchor="center",
            justify="center"
        )
        titulo.place(relx=0.5, rely=0.2, anchor="center")

        # Imagem Modo Claro
        claro = adicionar_imagem_texto(
            self,
            caminho_img="images/rezende.jpg",
            cor="transparent",
            tamanho=150,
            espacamento=20,
            texto="Modo Claro",
            cor_texto=None,
            comando=alternar_modo  # clique alterna o modo
        )
        claro.place(relx=0.2, rely=0.5, anchor=CENTER)

        # Imagem Modo Escuro
        escuro = adicionar_imagem_texto(
            self,
            caminho_img="images/rezende.jpg",
            cor="transparent",
            tamanho=150,
            espacamento=20,
            texto="Modo Escuro",
            cor_texto=None,
            comando=alternar_modo
        )
        escuro.place(relx=0.8, rely=0.5, anchor=CENTER)

        # Botão Avançar
        btn_selecionar = CTkButton(
            self,
            text="Avançar",
            font=("Arial", 15, "bold"),
            text_color="white",
            fg_color="#654E82",
            corner_radius=10,
            command=lambda: self.controller.mostrar_pagina("idioma_software")
        )
        btn_selecionar.place(relx=0.5, rely=0.8, anchor=CENTER)

        # Barra de progresso
        self.barra = progress_bar(self, cor_progresso="#C58ADE", modo="determinate", valor=0.2)
        self.barra.place(relx=0.5, rely=0.9, anchor=CENTER)
