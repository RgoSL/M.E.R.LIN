from customtkinter import *
from PIL import Image
from func_visual.funcs_imgs.imagem import adicionar_imagem_texto
from func_visual.widgets.progress import progress_bar
from func_visual.modos.ui_mode import alternar_modo  # função que alterna claro/escuro
from func_visual.widgets.header import nav

class modo_claro_escuro(CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        # Define cor inicial conforme modo atual
        
        # Cabeçalho
        nav(self,controller, "M.E.R.LIN")

        # Título
        self.titulo = CTkLabel(
            self,
            text="Modo Claro e Escuro",
            font=("Arial", 20, "bold"),
            text_color=None,
            anchor="center",
            justify="center"
        )
        self.titulo.place(relx=0.5, rely=0.2, anchor="center")

        # Imagem Modo Claro
        claro = adicionar_imagem_texto(
            self,
            caminho_img="assets/ImgsTemp/placeholder.jpg",
            cor="transparent",
            tamanho=150,
            espacamento=20,
            texto="Modo Claro",
            cor_texto=None,
            comando=self.trocar_modo  # ⚠️ agora chama método interno
        )
        claro.place(relx=0.2, rely=0.5, anchor=CENTER)

        # Imagem Modo Escuro
        escuro = adicionar_imagem_texto(
            self,
            caminho_img="assets/ImgsTemp/placeholder.jpg",
            cor="transparent",
            tamanho=150,
            espacamento=20,
            texto="Modo Escuro",
            cor_texto=None,
            comando=self.trocar_modo  # mesmo aqui
        )
        escuro.place(relx=0.8, rely=0.5, anchor=CENTER)

        # Botão Avançar
        btn_selecionar = CTkButton(self,text="Avançar", text_color = "#FFFFFF", font=("Bold", 15), fg_color = "#654E82", bg_color = "transparent", corner_radius = 10, height= 40, width= 143, hover_color = "#56397C", command=lambda: self.controller.mostrar_pagina("configSo"))
        btn_selecionar.place(relx=0.5, rely=0.8, anchor=CENTER)

        # Barra de progresso
        self.barra = progress_bar(self, cor_progresso="#C58ADE", modo="determinate", valor=0.2)
        self.barra.place(relx=0.5, rely=0.9, anchor=CENTER)

    def trocar_modo(self):
        """Alterna o modo e atualiza a cor de fundo da página."""
        alternar_modo()  # troca Light/Dark globalmente

        # Atualiza cor da página atual
        modo_atual = get_appearance_mode()
        self.cor_fundo = "#FFFFFF" if modo_atual == "Light" else "#2B2B2B"
        self.configure(fg_color=self.cor_fundo)

        # 🔥 Atualiza todas as páginas do app
        self.controller.atualizar_tema()