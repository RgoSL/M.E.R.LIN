import textwrap

from customtkinter import *
from func_visual.widgets.header import nav
from PIL import Image, ImageDraw, ImageFont, ImageTk
from func_visual.widgets.i18n import i18n


class termos_de_uso(CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        nav(self, controller, "M.E.R.LIN")

        self.label_titulo = CTkLabel(self, text="", anchor="center")
        self.label_titulo.place(relx=0.5, rely=0.2, anchor="center")

        self.quad = CTkScrollableFrame(
            self,
            fg_color="#654E82",
            scrollbar_button_color="#F9B14F",
            scrollbar_button_hover_color="#CE8E34",
            corner_radius=15,
            border_width=2,
        )
        self.quad.place(relx=0.5, rely=0.6, relwidth=0.85, relheight=0.6, anchor=CENTER)

        self.label_subtitulo = CTkLabel(self.quad, text="", anchor="center")
        self.label_subtitulo.pack(pady=10, padx=5)

        self.label_conteudo = CTkLabel(self.quad, text="", anchor="nw")
        self.label_conteudo.pack(pady=10, padx=5)

        icone_voltar = CTkImage(
            Image.open("assets/ImgsTemp/seta_esquerda.png"), size=(20, 20)
        )
        self.btn_voltar = CTkButton(
            self,
            image=icone_voltar,
            text="",
            fg_color="#654E82",
            hover_color="#56397C",
            command=lambda: self.controller.mostrar_pagina("ajustes"),
        )
        self.btn_voltar.place(
            relx=0.07, rely=0.15, anchor="center", relwidth=0.05, relheight=0.06
        )

        self.criar_imagens_texto()

    def criar_imagem_titulo(self):
        img_titulo = Image.new("RGBA", (600, 100), (0, 0, 0, 0))
        draw_titulo = ImageDraw.Draw(img_titulo)
        fonte_gideon = ImageFont.truetype("assets/fonts/GideonRoman-Regular.ttf", 40)
        
        texto = i18n.t("titulo_termos")
        draw_titulo.text((10, 10), texto, font=fonte_gideon, fill="#654E82")
        
        img_tk_titulo = ImageTk.PhotoImage(img_titulo)
        self.label_titulo.configure(image=img_tk_titulo)
        self.label_titulo.image = img_tk_titulo  

    def criar_imagem_subtitulo(self):
        img_termos = Image.new("RGBA", (600, 40), (0, 0, 0, 0))
        draw_termos = ImageDraw.Draw(img_termos)
        fonte_gideon = ImageFont.truetype("assets/fonts/GideonRoman-Regular.ttf", 30)
        
        texto = i18n.t("ajuste_termos")
        draw_termos.text((10, 5), texto, font=fonte_gideon, fill="#CB91E4")
        
        img_tk_termos = ImageTk.PhotoImage(img_termos)
        self.label_subtitulo.configure(image=img_tk_termos)
        self.label_subtitulo.image = img_tk_termos 

    def criar_imagem_conteudo(self):
        termos_texto = i18n.t("texto_termos")
        
        wrapper = textwrap.TextWrapper(width=60)
        termos_texto_quebrado = wrapper.fill(text=termos_texto)
        
        linhas = termos_texto_quebrado.count('\n') + 1
        altura_necessaria = max(200, linhas * 20 + 20)  
        
        img_texto = Image.new("RGBA", (600, altura_necessaria), (0, 0, 0, 0))
        draw_texto = ImageDraw.Draw(img_texto)
        fonte_gowun = ImageFont.truetype("assets/fonts/GowunDodum-Regular.ttf", 15)
        
        draw_texto.text(
            (10, 10), termos_texto_quebrado, font=fonte_gowun, fill="#E6C8FA"
        )
        
        img_tk_texto = ImageTk.PhotoImage(img_texto)
        self.label_conteudo.configure(image=img_tk_texto)
        self.label_conteudo.image = img_tk_texto 

    def criar_imagens_texto(self):
        self.criar_imagem_titulo()
        self.criar_imagem_subtitulo()
        self.criar_imagem_conteudo()

    def atualizar_idioma(self):
        self.criar_imagens_texto()
        print(f"Página termos_de_uso atualizada para idioma: {i18n.idioma_atual}")