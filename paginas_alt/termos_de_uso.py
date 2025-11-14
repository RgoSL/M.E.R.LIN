from PIL import Image, ImageDraw, ImageFont, ImageTk
from customtkinter import *
from func_visual.widgets.header import nav
import textwrap 

class termos_de_uso(CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        nav(self, controller, "M.E.R.LIN")

        img_titulo = Image.new("RGBA", (600, 100), (0, 0, 0, 0))
        draw_titulo = ImageDraw.Draw(img_titulo)
        fonte_gideon = ImageFont.truetype("assets/fonts/GideonRoman-Regular.ttf", 40)
        draw_titulo.text((10, 10), "Nossas Regras", font=fonte_gideon, fill="#FFFFFF")
        img_tk_titulo = ImageTk.PhotoImage(img_titulo)

        Titulo = CTkLabel(self, image=img_tk_titulo, text="", anchor="center")
        Titulo.image = img_tk_titulo  
        Titulo.place(relx=0.5, rely=0.2, anchor="center")

        quad = CTkScrollableFrame(self, fg_color="#654E82", scrollbar_button_color= "#F9B14F", scrollbar_button_hover_color= "#CE8E34", corner_radius=15, border_width=2)
        quad.place(relx=0.5, rely=0.6, relwidth=0.85, relheight=0.6, anchor=CENTER)

        img_termos = Image.new("RGBA", (600, 40), (0, 0, 0, 0))
        draw_termos = ImageDraw.Draw(img_termos)
        fonte_gideon = ImageFont.truetype("assets/fonts/GideonRoman-Regular.ttf", 30)
        draw_termos.text((10, 5), "Termos de Uso", font=fonte_gideon, fill="#CB91E4")
        img_tk_termos = ImageTk.PhotoImage(img_termos)

        txt_termos = CTkLabel(quad, image=img_tk_termos, text="", anchor="center")
        txt_termos.image = img_tk_termos 
        txt_termos.pack(pady=10, padx=5)

        termos_texto = ("Ao utilizar o M.E.R.LIN, você concorda com os seguintes termos e condições. "
                        "Nosso serviço é projetado para melhorar a acessibilidade e a interação por meio de recursos "
                        "de webcam, respeitando a sua privacidade e segurança. É importante que você tenha ciência de "
                        "que coletamos dados de vídeo apenas para a finalidade de fornecer a funcionalidade do serviço, "
                        "com total transparência e conformidade com as regulamentações de privacidade.")
        
        wrapper = textwrap.TextWrapper(width=60) 
        termos_texto_quebrado = wrapper.fill(text=termos_texto)  

        img_texto = Image.new("RGBA", (600, 200), (0, 0, 0, 0))
        draw_texto = ImageDraw.Draw(img_texto)
        fonte_gowun = ImageFont.truetype("assets/fonts/GowunDodum-Regular.ttf", 15)

        draw_texto.text((10, 10), termos_texto_quebrado, font=fonte_gowun, fill="#E6C8FA")
        img_tk_texto = ImageTk.PhotoImage(img_texto)

        txt_termos_conteudo = CTkLabel(quad, image=img_tk_texto, text="", anchor="nw")
        txt_termos_conteudo.image = img_tk_texto  
        txt_termos_conteudo.pack(pady=10, padx=5)

        icone_voltar = CTkImage(Image.open("assets/ImgsTemp/seta_esquerda.png"), size=(20, 20))
        btntst = CTkButton(
            self,
            image=icone_voltar,
            text="",
            fg_color="#654E82",
            hover_color="#56397C",
            command=lambda: self.controller.mostrar_pagina("ajustes")
        )

        btntst.place(relx=0.07, rely=0.15, anchor="center", relwidth=0.05, relheight=0.06)

        self.img_tk_titulo = img_tk_titulo
        self.img_tk_termos = img_tk_termos
        self.img_tk_texto = img_tk_texto