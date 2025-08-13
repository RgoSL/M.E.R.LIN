from customtkinter import *
from PIL import Image
import os
from func_visual.funcs_imgs.imagem import adcionar_logo

class config(CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        # Frame roxo de fundo total
        frame = CTkFrame(self, fg_color="#FFFFFF", corner_radius=0)
        frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        logo = adcionar_logo(
            self, 
            caminho_img="images/logo.png", 
            texto="Sua História começa aqui", 
            cor="#FFFFFF", 
            tamanho=160, 
            espacamento=10,
            cor_texto="black"
        )

        logo.place(relx=0.2, rely=0.5, anchor=CENTER)
        # header

        header = CTkFrame(self, fg_color="#654E82", corner_radius=0)
        header.place(relx=0, rely=0, relwidth=1, relheight=0.1)

        txt_logo = CTkLabel(header, text="M.E.R.LIN", font=("Bold", 20), text_color="#E6C8FA")
        txt_logo.place(relx=0.1, rely=0.5, anchor=CENTER)

        label = CTkLabel(header, text="Escolha como se preparar", font=("Bold", 20), text_color="black")
        label.place(relx=0.5, rely=0.5, anchor=CENTER)

        Label2 = CTkLabel(self, text="Tipo de Configuração:", font=("Bold", 18), text_color="black",bg_color="white")
        Label2.place(relx=0.62, rely=0.35, anchor=CENTER)

        radio_var = IntVar()

        # Primeira opção
        frame_check = CTkFrame(self, fg_color="white", corner_radius=15, border_color="#C58ADE", border_width=2,bg_color="white")
        frame_check.place(relx=0.7, rely=0.45, relwidth=0.4, relheight=0.13, anchor=CENTER)

        radio1 = CTkRadioButton(frame_check, text="Opção 1", font=("Bold", 15), text_color="black",
                                variable=radio_var, value=1, fg_color="#654E82")
        radio1.place(relx=0.2, rely=0.5, anchor=CENTER)

        # Segunda opção
        frame_check2 = CTkFrame(self, fg_color="white", corner_radius=15, border_color="#C58ADE", border_width=2,bg_color="white")
        frame_check2.place(relx=0.7, rely=0.6, relwidth=0.4, relheight=0.13, anchor=CENTER)

        radio2 = CTkRadioButton(frame_check2, text="Opção 2", font=("Bold", 15), text_color="black",
                                variable=radio_var, value=2, fg_color="#654E82")
        radio2.place(relx=0.2, rely=0.5, anchor=CENTER)

        # Botões
        btn_voltar = CTkButton(self, text="Voltar", font=("Bold", 15), text_color="white", fg_color="#654E82",corner_radius=10, command=lambda: controller.mostrar_pagina("inicial"), hover=False)
        
        btn_proximo = CTkButton(self, text="Proximo",  font=("Bold", 15), text_color="white", fg_color="#654E82",corner_radius=10,command=lambda: controller.mostrar_pagina("ajustes"), hover=False)
        
        btn_voltar.place(relx=0.15, rely=0.9, anchor=CENTER, relwidth=0.2, relheight=0.06)
        btn_proximo.place(relx=0.85, rely=0.9, anchor=CENTER, relwidth=0.2, relheight=0.06)

        # Barra de progresso
        progress_bar = CTkProgressBar(self, mode="determinate", width=200, height=20,
                                      fg_color="#654E82", progress_color="#C58ADE")
        progress_bar.place(relx=0.5, rely=0.9, anchor=CENTER, relwidth=0.4, relheight=0.03)

      