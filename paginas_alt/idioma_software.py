from customtkinter import *
from func_visual.funcs_imgs.imagem import adicionar_imagem_texto
from func_visual.widgets.header import nav
from func_visual.widgets.lista_idiomas import criar_lista_idiomas, idiomas
from func_visual.widgets.progress import progress_bar
from PIL import Image, ImageDraw, ImageFont, ImageTk
from func_visual.widgets.i18n import i18n

class idioma_software(CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        
        # Método Para Definir Essa Tela Como um Frame Tradutível
        i18n.registrar_observer(self)
        
        nav(self, controller, "M.E.R.LIN")

        self.logo = adicionar_imagem_texto(
            self,
            caminho_img_dark="assets/ImgsConfig/idiomaImgEscuro.png",
            caminho_img_light="assets/ImgsConfig/idiomaImg.png",
            texto=" ",
            cor="transparent",
            tamanho=160,
            espacamento=10,
            cor_texto=None,
        )
        self.logo.place(relx=0.2, rely=0.5, anchor="center")

        self.criar_titulo_principal()

        self.criar_subtitulo()

        self.quad = CTkScrollableFrame(
            self,
            fg_color="white",
            corner_radius=15,
            border_color="#C58ADE",
            border_width=2,
            scrollbar_button_color="#C58ADE",
            scrollbar_button_hover_color="#654E82",
        )
        self.quad.place(
            relx=0.65, rely=0.5, relwidth=0.5, relheight=0.25, anchor="center"
        )

        self.labels_idiomas = criar_lista_idiomas(
            self.quad, 
            idiomas, 
            callback=self.ao_selecionar_idioma 
        )

        self.btn_voltar = CTkButton(
            self,
            text=i18n.t("voltar"),
            font=("Gideon Roman", 20),
            height=40,
            width=60,
            text_color="#FFFFFF",
            bg_color="transparent",
            fg_color="#654E82",
            corner_radius=10,
            hover_color="#56397C",
            command=lambda: controller.mostrar_pagina("bemVindo"),
        )

        self.btn_proximo = CTkButton(
            self,
            text=i18n.t("avancar"),
            font=("Gideon Roman", 20),
            text_color="#FFFFFF",
            height=40,
            width=60,
            bg_color="transparent",
            fg_color="#654E82",
            corner_radius=10,
            hover_color="#56397C",
            command=lambda: controller.mostrar_pagina("configSo"),
        )

        self.btn_voltar.place(
            relx=0.15, rely=0.9, anchor="center", relwidth=0.2, relheight=0.06
        )
        self.btn_proximo.place(
            relx=0.85, rely=0.9, anchor="center", relwidth=0.2, relheight=0.06
        )

        self.barra = progress_bar(
            self, cor_progresso="#C58ADE", modo="determinate", valor=0.1
        )
        self.barra.place(relx=0.5, rely=0.9, anchor="center")

    def criar_titulo_principal(self):
        img = Image.new("RGBA", (1200, 120), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        fonte_personalizada = ImageFont.truetype(
            "assets/fonts/GideonRoman-Regular.ttf", 30
        )
        
        texto = i18n.t("titulo_idiomas")
        draw.text((10, 10), texto, font=fonte_personalizada, fill="#654E82")
        
        self.txt_selecao_img = ImageTk.PhotoImage(img)
        
        if hasattr(self, 'Txt_selecao'):
            self.Txt_selecao.configure(image=self.txt_selecao_img)
        else:
            self.Txt_selecao = CTkLabel(
                self, image=self.txt_selecao_img, text="", bg_color="transparent"
            )
            self.Txt_selecao.place(relx=0.87, rely=0.23, anchor="center")

    def criar_subtitulo(self):
        img2 = Image.new("RGBA", (700, 80), (0, 0, 0, 0))
        draw2 = ImageDraw.Draw(img2)
        fonte_subtitulo = ImageFont.truetype("assets/fonts/GideonRoman-Regular.ttf", 18)
        
        texto_sub = i18n.t("idioma_software")
        draw2.text((5, 5), texto_sub, font=fonte_subtitulo, fill="#654E82")
        
        self.txt_subtitulo_img = ImageTk.PhotoImage(img2)
        
        if hasattr(self, 'subtitulo'):
            self.subtitulo.configure(image=self.txt_subtitulo_img)
        else:
            self.subtitulo = CTkLabel(
                self, image=self.txt_subtitulo_img, text="", bg_color="transparent"
            )
            self.subtitulo.place(relx=0.84, rely=0.38, anchor="center")

    def ao_selecionar_idioma(self, codigo_idioma):
        print(f"Idioma selecionado: {codigo_idioma}")
        i18n.mudar_idioma(codigo_idioma)
        
        self.salvar_preferencia_idioma(codigo_idioma)

    def atualizar_idioma(self):
        self.criar_titulo_principal()
        self.criar_subtitulo()
        
        self.btn_voltar.configure(text=i18n.t("voltar"))
        self.btn_proximo.configure(text=i18n.t("avancar"))
        
        self.atualizar_labels_idiomas()

    def atualizar_labels_idiomas(self):
        nomes_idiomas = {
            "pt": "portugues",
            "en": "ingles",
            "es": "espanhol"
        }
        
        for codigo, label in self.labels_idiomas:
            nome_traduzido = i18n.t(nomes_idiomas.get(codigo, codigo))
            label.configure(text=f"{nome_traduzido} ({codigo.upper()})")

    def salvar_preferencia_idioma(self, codigo_idioma):

        try:
            import json
            import os
            
            config_path = "config/preferencias.json"
            
            os.makedirs(os.path.dirname(config_path), exist_ok=True)

            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
            else:
                config = {}
            
            config['idioma'] = codigo_idioma
            
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
                
            print(f"Idioma {codigo_idioma} salvo com sucesso!")
            
        except Exception as e:
            print(f"Erro ao salvar preferência de idioma: {e}")

    def __del__(self):
        i18n.remover_observer(self)