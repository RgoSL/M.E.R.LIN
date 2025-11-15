from customtkinter import *
from PIL import Image, ImageDraw, ImageFont, ImageTk
import tkinter.font as tkfont
import os

from func_visual.funcs_imgs.imagem import adicionar_imagem_texto
from func_visual.widgets.progress import progress_bar
from func_visual.modos.ui_mode import alternar_modo  # função que alterna claro/escuro
from func_visual.widgets.header import nav


class modo_claro_escuro(CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        
        # Tenta registrar fontes (ainda útil para os botões)
        try:
            self.debug_fonts()
        except Exception as e:
            print("⚠️ Erro ao achar a fonte:", e)
        
        # Cabeçalho
        nav(self, controller, "M.E.R.LIN")

        # --------------------------
        # 🖋️ Renderiza o título com PIL e a fonte GideonRoman
        # --------------------------
        self.titulo_label = self.criar_titulo_imagem(
            texto="Estilo é Poder. Qual o Seu?",
            tamanho=30,
            cor="#FFFFFF",
            largura=700,
            altura=120
        )
        self.titulo_label.place(relx=0.5, rely=0.2, anchor="center")

        # Imagem Modo Claro
        claro = adicionar_imagem_texto(
            self,
            caminho_img="assets/ImgsTemp/placeholder.jpg",
            cor="transparent",
            tamanho=150,
            espacamento=20,
            texto="Tema Claro",
            cor_texto=None,
            comando=self.trocar_modo
        )
        claro.place(relx=0.2, rely=0.5, anchor=CENTER)

        # Imagem Modo Escuro
        escuro = adicionar_imagem_texto(
            self,
            caminho_img="assets/ImgsTemp/placeholder.jpg",
            cor="transparent",
            tamanho=150,
            espacamento=20,
            texto="Tema Escuro",
            cor_texto=None,
            comando=self.trocar_modo
        )
        escuro.place(relx=0.8, rely=0.5, anchor=CENTER)

        # Barra de progresso
        self.barra = progress_bar(self, cor_progresso="#C58ADE", modo="determinate", valor=0.2)
        self.barra.place(relx=0.5, rely=0.9, anchor=CENTER)

        # --------------------------
        # Botões de Navegação (Voltar e Avançar)
        # --------------------------

        # Botão Voltar
        btn_voltar = CTkButton(
            self,
            text="Voltar",
            text_color="#FFFFFF",
            fg_color="#654E82",
            font=("GowunDodum", 17),
            bg_color="transparent",
            corner_radius=10,
            height=36,
            width=160,
            hover_color="#56397C",
            command=lambda: self.controller.mostrar_pagina("config")
        )
        btn_voltar.place(relx=0.05, rely=0.9, anchor="w")

        # Botão Avançar (Repetição do botão anterior)
        btn_avancar = CTkButton(
            self,
            text="Avançar",
            text_color="#FFFFFF",
            fg_color="#654E82",
            font=("GowunDodum", 17),
            bg_color="transparent",
            corner_radius=10,
            height=36,
            width=160,
            hover_color="#56397C",
            command=lambda: self.controller.mostrar_pagina("ajustes")
        )
        btn_avancar.place(relx=0.95, rely=0.9, anchor="e")


    # ---------------------------------------
    # 🧠 Cria imagem de texto com fonte real (PIL)
    # ---------------------------------------
    def criar_titulo_imagem(self, texto, tamanho, cor, largura, altura):
        """Renderiza texto com a fonte GideonRoman e retorna um CTkLabel com imagem."""
        fonte_path = os.path.join("assets", "Fonts", "GideonRoman-Regular.ttf")

        # Cria imagem transparente
        img = Image.new("RGBA", (largura, altura), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Carrega a fonte diretamente do arquivo .ttf
        fonte_gideon = ImageFont.truetype(fonte_path, tamanho)

        # Centraliza o texto
        bbox = draw.textbbox((0, 0), texto, font=fonte_gideon)
        texto_largura = bbox[2] - bbox[0]
        texto_altura = bbox[3] - bbox[1]
        pos_x = (largura - texto_largura) // 2
        pos_y = (altura - texto_altura) // 2

        # Desenha o texto
        draw.text((pos_x, pos_y), texto, font=fonte_gideon, fill=cor)

        # Converte pra imagem Tkinter
        img_tk = ImageTk.PhotoImage(img)

        # Retorna um label que exibe a imagem
        label_img = CTkLabel(self, image=img_tk, text="")
        label_img.image = img_tk  # mantém referência para não ser coletado

        return label_img


    # ---------------------------------------
    def debug_fonts(self):
        """Cria fontes Tk (para botões e outros textos padrão)."""
        font_src = os.path.join("assets", "Fonts")
        Gideon = os.path.join(font_src, "GideonRoman-Regular.ttf")
        Gowun = os.path.join(font_src, "GowunDodum-Regular.ttf")

        self.tk.call("font", "create", "GideonRoman", "-family", "GideonRoman", "-size", 12)
        self.tk.call("font", "create", "GowunDodum", "-family", "GowunDodum", "-size", 12)


    def trocar_modo(self):
        """Alterna o modo e atualiza a cor de fundo da página."""
        alternar_modo()  # troca Light/Dark globalmente

        # Atualiza cor da página atual
        modo_atual = get_appearance_mode()
        self.cor_fundo = "#FFFFFF" if modo_atual == "Light" else "#2B2B2B"
        self.configure(fg_color=self.cor_fundo)

        # 🔥 Atualiza todas as páginas do app
        self.controller.atualizar_tema()