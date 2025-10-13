from customtkinter import *
from PIL import Image
from func_visual.funcs_imgs.imagem import adicionar_imagem_texto
from func_visual.widgets.progress import progress_bar
from func_visual.widgets.lista_idiomas import criar_lista_idiomas, idiomas

class idioma_software(CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        header = CTkFrame(self, fg_color="#654E82", corner_radius=0)
        header.place(relx=0, rely=0, relwidth=1, relheight=0.1)

        titulo = CTkLabel(
            header,
            text="Toda a magia começa pelas palarvas certas",
            font=("Arial", 20, "bold"),
            text_color="#E6C8FA",
        )
        titulo.place(relx=0.5, rely=0.5, anchor="center")

        logo = adicionar_imagem_texto(
            self, 
            caminho_img="images/placeholder.jpg", 
            texto=" ", 
            cor="transparent", 
            tamanho=160, 
            espacamento=10,
            cor_texto=None
        )

        logo.place(relx=0.2, rely=0.5, anchor=CENTER)

        Txt_selecao = CTkLabel(self, text="Selecione o idioma do software:", font=("Bold", 20), text_color=None, bg_color="transparent")
        Txt_selecao.place(relx=0.57, rely=0.2, anchor=CENTER)

        quad = CTkScrollableFrame(self, fg_color="white", corner_radius=15, border_color="#C58ADE", border_width=2, scrollbar_button_color="#C58ADE", scrollbar_button_hover_color="#654E82")
        quad.place(relx=0.65, rely=0.5, relwidth=0.5, relheight=0.5, anchor=CENTER)

        criar_lista_idiomas(quad, idiomas, padding_y=10)

        btn_voltar = CTkButton(self, text="Voltar", font=("Bold", 15), text_color="white",bg_color="transparent" ,fg_color="#654E82",corner_radius=10, command=lambda: controller.mostrar_pagina("modo_claro_escuro"), hover=False)
        
        btn_proximo = CTkButton(self, text="Proximo",  font=("Bold", 15), text_color="white",bg_color="transparent" ,fg_color="#654E82",corner_radius=10,command=lambda: controller.mostrar_pagina("config"), hover=False)
        
        btn_voltar.place(relx=0.15, rely=0.9, anchor=CENTER, relwidth=0.2, relheight=0.06)
        btn_proximo.place(relx=0.85, rely=0.9, anchor=CENTER, relwidth=0.2, relheight=0.06)

        # Barra de progresso
        self.barra = progress_bar(self,cor_progresso="#C58ADE",modo="determinate",valor=0.5)
        self.barra.place(relx=0.5, rely=0.9, anchor=CENTER)