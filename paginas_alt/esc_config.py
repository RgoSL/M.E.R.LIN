from customtkinter import *
from PIL import Image
import os
from func_visual.funcs_imgs.imagem import adicionar_imagem_texto
from func_visual.widgets.progress import progress_bar
from func_visual.widgets.header import nav

class config(CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        logo = adicionar_imagem_texto(
            self, 
            caminho_img="assets/ImgsTemp/placeholder.jpg", 
            texto="Sua História começa aqui", 
            cor="transparent", 
            tamanho=160, 
            espacamento=10,
            cor_texto=None
        )

        logo.place(relx=0.2, rely=0.5, anchor=CENTER)
        # header

        nav(self,controller, "M.E.R.LIN")

        label = CTkLabel(self, text="Escolha como se preparar", font=("Bold", 20), text_color=None, bg_color="transparent")
        label.place(relx=0.5, rely=0.15, anchor=CENTER)

        Label2 = CTkLabel(self, text="Tipo de Configuração:", font=("Bold", 18), text_color=None,bg_color="transparent")
        Label2.place(relx=0.62, rely=0.35, anchor=CENTER)

        radio_var = IntVar()

        # Primeira opção
        frame_check = CTkFrame(self, fg_color="white", corner_radius=15, border_color="#C58ADE", border_width=2,bg_color="transparent")
        frame_check.place(relx=0.7, rely=0.45, relwidth=0.4, relheight=0.13, anchor=CENTER)

        radio1 = CTkRadioButton(frame_check, text="Normal", font=("Bold", 15), text_color="black",
                                variable=radio_var, value=1, fg_color="#654E82")
        radio1.place(relx=0.2, rely=0.5, anchor=CENTER)

        # Segunda opção
        frame_check2 = CTkFrame(self, fg_color="white", corner_radius=15, border_color="#C58ADE", border_width=2,bg_color="transparent")
        frame_check2.place(relx=0.7, rely=0.6, relwidth=0.4, relheight=0.13, anchor=CENTER)

        radio2 = CTkRadioButton(frame_check2, text="Avançada", font=("Bold", 15), text_color="black",
                                variable=radio_var, value=2, fg_color="#654E82")
        radio2.place(relx=0.2, rely=0.5, anchor=CENTER)

        # Botões
        btn_voltar = CTkButton(self, text="Voltar", font=("Bold", 15), text_color="#FFFFFF",bg_color="transparent", height=40, width=60, fg_color="#654E82",corner_radius=10, hover_color= "#56397C", command=lambda: controller.mostrar_pagina("idioma_software"))
        
        btn_proximo = CTkButton(self, text="Avançar",  font=("Bold", 15), text_color="#FFFFFF",bg_color="transparent", height=40, width=60,fg_color="#654E82",corner_radius=10,  hover_color= "#56397C", command=lambda: controller.mostrar_pagina("ajustes"))
        
        btn_voltar.place(relx=0.15, rely=0.9, anchor=CENTER, relwidth=0.2, relheight=0.06)
        btn_proximo.place(relx=0.85, rely=0.9, anchor=CENTER, relwidth=0.2, relheight=0.06)

        # Barra de progresso
        self.barra = progress_bar(self,cor_progresso="#C58ADE",modo="determinate",valor=0.8)
        self.barra.place(relx=0.5, rely=0.9, anchor=CENTER)