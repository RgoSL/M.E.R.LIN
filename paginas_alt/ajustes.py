from customtkinter import *
from PIL import Image
import os
from func_visual.widgets.header import nav
from func_nao_visual.Banco.preferencias import criar_tabela, salvar_ajustes, carregar_ajustes
from func_visual.widgets.progress import progress_bar

class ajustes(CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        criar_tabela()  

        nav(self, controller, "M.E.R.LIN")

        titulo = CTkLabel(self, text="Ajustes", font=("Gideon Roman", 30), text_color="white")
        titulo.place(relx=0.5, rely=0.2, anchor=CENTER)

        frame2 = CTkFrame(self, fg_color="#654E82", corner_radius=20)
        frame2.place(relx=0.5, rely=0.62, relwidth=0.82, relheight=0.58, anchor=CENTER)
        self.frame2 = frame2

        dados = carregar_ajustes()
        if dados:
            resolucao_sel, idioma_sel, fps_sel, luz_sel = dados
        else:
            resolucao_sel, idioma_sel, fps_sel, luz_sel = "Resolução", "Idiomas", "FPS", "Luz da Camera"

        menu_h = 0.12
        menu_w = 0.20
        fonte_itens = ("Arial", 17)

        # OPTION MENU FIX — sem border_width
        opt_cfg = {
            "command": self.salvar_config,
            "fg_color": "#E6C8FA",
            "dropdown_fg_color": "#654E82",
            "text_color": "black",
            "button_hover_color": "#56397C",
            "button_color": "#E6C8FA",
            "font": fonte_itens
        }

        self.OptionMenu5 = CTkOptionMenu(frame2, values=["Luz da Camera", "Sim", "Não"], **opt_cfg)
        self.OptionMenu5.set(luz_sel)
        self.OptionMenu5.place(relx=0.23, rely=0.27, anchor=W, relwidth=menu_w, relheight=menu_h)

        self.OptionMenu1 = CTkOptionMenu(frame2, values=["Resolução", "1080p", "720p", "360p"], **opt_cfg)
        self.OptionMenu1.set(resolucao_sel)
        self.OptionMenu1.place(relx=0.47, rely=0.27, anchor=W, relwidth=menu_w, relheight=menu_h)

        self.OptionMenu3 = CTkOptionMenu(frame2, values=["FPS", "120 fps", "60 fps", "30 fps"], **opt_cfg)
        self.OptionMenu3.set(fps_sel)
        self.OptionMenu3.place(relx=0.71, rely=0.27, anchor=W, relwidth=menu_w, relheight=menu_h)

        self.OptionMenu2 = CTkOptionMenu(frame2, values=["Idiomas", "Português", "Inglês", "Espanhol"], **opt_cfg)
        self.OptionMenu2.set(idioma_sel)
        self.OptionMenu2.place(relx=0.23, rely=0.48, anchor=W, relwidth=0.68, relheight=menu_h)


        camera = CTkLabel(frame2, text="Câmera", font=("Arial", 17), text_color="#E6C8FA")
        camera.place(relx=0.12, rely=0.23, anchor=W)

        lingua = CTkLabel(frame2, text="Língua", font=("Arial", 17), text_color="#E6C8FA")
        lingua.place(relx=0.12, rely=0.44, anchor=W)

        termos_de_uso = CTkLabel(frame2, text="Termos de Uso", font=("Arial", 16),
                                 text_color="#E6C8FA", cursor="hand2")
        termos_de_uso.place(relx=0.15, rely=0.9, anchor=CENTER)
        termos_de_uso.bind("<Button-1>", lambda e: self.controller.mostrar_pagina("termos_de_uso"))

        self.barra = progress_bar(self, cor_progresso="#C58ADE", modo="determinate", valor=1)
        self.barra.place(relx=0.5, rely=0.95, anchor=CENTER)

        # ICONES COMO CTkImage (corrige DPI + hover completo)
        icone_voltar = CTkImage(Image.open("assets/ImgsTemp/seta_esquerda.png"), size=(26, 26))
        icone_avanc = CTkImage(Image.open("assets/ImgsTemp/seta_direita.png"), size=(26, 26))

        btn_voltar = CTkButton(self, image=icone_voltar, text="", fg_color="#654E82",
                               hover_color="#56397C",
                               width=50, height=50,
                               command=lambda: controller.mostrar_pagina("modo_claro_escuro"))
        btn_voltar.place(relx=0.07, rely=0.20, anchor=CENTER)

        avanc = CTkButton(self, image=icone_avanc, text="", fg_color="#654E82",
                          hover_color="#56397C",
                          width=50, height=50,
                          command=lambda: controller.mostrar_pagina("inicial"))
        avanc.place(relx=0.9, rely=0.20, anchor=CENTER)

    def salvar_config(self, _=None):
        salvar_ajustes(
            self.OptionMenu1.get(),
            self.OptionMenu2.get(),
            self.OptionMenu3.get(),
            self.OptionMenu5.get()
        )

    def atualizar_info_label(self):
        pass