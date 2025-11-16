from customtkinter import *
from PIL import Image, ImageDraw, ImageFont, ImageTk
from func_visual.funcs_imgs.imagem import adicionar_imagem_texto
from func_visual.widgets.progress import progress_bar
from func_visual.widgets.lista_idiomas import criar_lista_idiomas, idiomas
from func_visual.widgets.header import nav

class idioma_software(CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.idioma_atual = "pt"  # idioma padrão

        nav(self, controller, "M.E.R.LIN")

        self.logo = adicionar_imagem_texto(
            self, caminho_img="assets/ImgsTemp/placeholder.jpg", texto=" ", cor="transparent",
            tamanho=160, espacamento=10, cor_texto=None
        )
        self.logo.place(relx=0.2, rely=0.5, anchor="center")

        # ==========================================
        # TEXTO PRINCIPAL ESTILIZADO COM FONTE REAL
        # ==========================================
        img = Image.new("RGBA", (1200, 120), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        fonte_personalizada = ImageFont.truetype(
            "assets/fonts/GideonRoman-Regular.ttf", 30)

        texto = "Toda Magia Começa Pelas Palavras Certas"

        draw.text(
            (10, 10),
            texto,
            font=fonte_personalizada,
            fill="#654E82"
        )

        self.txt_selecao_img = ImageTk.PhotoImage(img)

        self.Txt_selecao = CTkLabel(
            self,
            image=self.txt_selecao_img,
            text="",
            bg_color="transparent"
        )
        self.Txt_selecao.place(relx=0.87, rely=0.23, anchor="center")

        # ==========================================
        # SUBTÍTULO ACIMA DA LISTA DE IDIOMAS
        # ==========================================
        img2 = Image.new("RGBA", (700, 80), (0, 0, 0, 0))
        draw2 = ImageDraw.Draw(img2)

        fonte_subtitulo = ImageFont.truetype("assets/fonts/GideonRoman-Regular.ttf", 18)

        texto_sub = "Idioma do Software:"

        draw2.text(
            (5, 5),
            texto_sub,
            font=fonte_subtitulo,
            fill="#654E82"
        )

        self.txt_subtitulo_img = ImageTk.PhotoImage(img2)

        self.subtitulo = CTkLabel(
            self,
            image=self.txt_subtitulo_img,
            text="",
            bg_color="transparent"
        )
        self.subtitulo.place(relx=0.84, rely=0.38, anchor="center")

        # ==========================================
        # QUADRO DE IDIOMAS
        # ==========================================
        self.quad = CTkScrollableFrame(
            self, fg_color="white", corner_radius=15,
            border_color="#C58ADE", border_width=2,
            scrollbar_button_color="#C58ADE",
            scrollbar_button_hover_color="#654E82"
        )
        self.quad.place(relx=0.65, rely=0.5, relwidth=0.5, relheight=0.25, anchor="center")

        criar_lista_idiomas(self.quad, idiomas, callback=None)

        self.btn_voltar = CTkButton(
            self, text="Voltar", font=("Bold", 15), height=40, width=60,
            text_color="#FFFFFF", bg_color="transparent",
            fg_color="#654E82", corner_radius=10, hover_color= "#56397C",
            command=lambda: controller.mostrar_pagina("bemVindo")
        )

        self.btn_proximo = CTkButton(
            self, text="Avançar", font=("Bold", 15), text_color="#FFFFFF",
            height=40, width=60, bg_color="transparent",
            fg_color="#654E82", corner_radius=10, hover_color="#56397C",
            command=lambda: controller.mostrar_pagina("configSo")
        )

        self.btn_voltar.place(relx=0.15, rely=0.9, anchor="center",
                              relwidth=0.2, relheight=0.06)
        self.btn_proximo.place(relx=0.85, rely=0.9, anchor="center",
                               relwidth=0.2, relheight=0.06)

        # Barra de progresso
        self.barra = progress_bar(self, cor_progresso="#C58ADE",
                                  modo="determinate", valor=0.1)
        self.barra.place(relx=0.5, rely=0.9, anchor="center")

    def mudar_idioma(self, novo_idioma):
        self.Txt_selecao.configure(
            text="Idioma do Software :"
        )
        self.btn_voltar.configure(text="voltar")
        self.btn_proximo.configure(text="Próximo")

        self.idioma_atual = novo_idioma
