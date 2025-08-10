# inicial.py
from customtkinter import *
from PIL import Image
from func_visual.imagem import adcionar_imagem

class inicial(CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        self.configure(fg_color="white")

        # Cabeçalho
        header = CTkFrame(self, fg_color="#654E82", corner_radius=0)
        header.place(relx=0, rely=0, relwidth=1, relheight=0.1)

        txt_logo = CTkLabel(header, text="M.E.R.LIN", font=("Bold", 20), text_color="#E6C8FA")
        txt_logo.place(relx=0.1, rely=0.5, anchor=CENTER)

        # Título
        Titulo = CTkLabel(
            self,
            text="Seus Controles",
            font=("Arial", 20, "bold"),
            text_color="black",
            anchor="center",
            justify="center"
        )
        Titulo.place(relx=0.5, rely=0.2, anchor="center")

        # Frame com rolagem horizontal
        frame1 = CTkScrollableFrame(
            self,
            fg_color="#654E82",
            corner_radius=5,
            orientation="horizontal",
            scrollbar_button_color="#F9B14F",
            scrollbar_button_hover_color="#F9B14F"
        )
        frame1.place(relx=0.1, rely=0.25, relwidth=0.8, relheight=0.5)

        # Container para organizar elementos horizontalmente
        content_frame = CTkFrame(frame1, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Botão de configurações
        btntst = CTkButton(
            self,
            text="Voltar",
            font=("Arial", 15),
            text_color="black",
            fg_color="#F9B14F",
            command=self.abrir_config,
        )
        btntst.place(relx=0.9, rely=0.15, anchor="center", relwidth=0.1, relheight=0.06)

        # Adicionar imagens horizontalmente
        adcionar_imagem(content_frame, "func_visual/rezende.jpg", texto_str="Imagem 1")
        adcionar_imagem(content_frame, "func_visual/rezende.jpg", texto_str="Imagem 2")
        adcionar_imagem(content_frame, "func_visual/rezende.jpg", texto_str="Imagem 3")

    def abrir_config(self):
        self.controller.mostrar_pagina("config")


# func_visual/imagem.py
from customtkinter import *
from PIL import Image

def adcionar_imagem(parent_frame, caminho_img, texto_str=" ", cor="transparent", largura=200, altura=160):
    """
    Função corrigida para adicionar imagens em layout horizontal
    """
    try:
        # Carregar e redimensionar a imagem
        img_pil = Image.open(caminho_img).convert("RGBA")
        img_pil = img_pil.resize((largura, altura), Image.Resampling.LANCZOS)
        img_ctk = CTkImage(light_image=img_pil, size=(largura, altura))

        # Container para imagem e texto
        container = CTkFrame(parent_frame, fg_color=cor, corner_radius=8)
        container.pack(side="left", padx=220, pady=10, fill="y")

        # Label da imagem
        img_label = CTkLabel(container, image=img_ctk, text="")
        img_label.image = img_ctk  # Manter referência
        img_label.pack(pady=(10, 5))

        # Texto abaixo da imagem
        if texto_str and texto_str.strip():
            texto = CTkLabel(
                container, 
                text=texto_str, 
                font=("Arial", 12), 
                text_color="white",  # Mudei para branco para contrastar com o fundo
                fg_color="transparent"
            )
            texto.pack(pady=(0, 10))
        else:
            texto = None

        return img_label, texto
        
    except Exception as e:
        print(f"Erro na função adcionar_imagem: {e}")
        # Criar um placeholder em caso de erro
        placeholder = CTkLabel(
            parent_frame, 
            text=f"Erro ao carregar\n{texto_str}", 
            width=largura, 
            height=altura,
            fg_color="gray"
        )
        placeholder.pack(side="left", padx=10, pady=10)
        return placeholder, None