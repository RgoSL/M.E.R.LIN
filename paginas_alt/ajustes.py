from customtkinter import *
from PIL import Image
import os
from func_visual.widgets.header import nav
from func_nao_visual.Banco.preferencias import criar_tabela, salvar_ajustes, carregar_ajustes

class ajustes(CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        criar_tabela()  # garante que o banco existe

        nav(self, controller, "M.E.R.LIN")

        titulo = CTkLabel(self, text="Ajustes", font=("Bold", 20))
        titulo.place(relx=0.5, rely=0.15, anchor=CENTER)

        frame2 = CTkFrame(self, fg_color="#654E82", corner_radius=15)
        frame2.place(relx=0.5, rely=0.6, relwidth=0.8, relheight=0.5, anchor=CENTER)
        self.frame2 = frame2  # referência pra usar depois

        # Carrega dados do banco
        dados = carregar_ajustes()
        if dados:
            resolucao_sel, idioma_sel, fps_sel, luz_sel = dados
        else:
            resolucao_sel, idioma_sel, fps_sel, luz_sel = "Resolução", "Idiomas", "FPS", "Luz da Camera"

        # --- OptionMenus colados lado a lado ---
        self.OptionMenu5 = CTkOptionMenu(frame2, values=["Luz da Camera","Sim", "Não"],
                                         command=self.salvar_config, fg_color="#E6C8FA",
                                         dropdown_fg_color="#654E82", text_color="black", button_color="#E6C8FA")
        self.OptionMenu5.set(luz_sel)
        self.OptionMenu5.place(relx=0.23, rely=0.3, anchor=W, relwidth=0.18, relheight=0.1)

        self.OptionMenu1 = CTkOptionMenu(frame2, values=["Resolução","1080p", "720p", "360p"],
                                         command=self.salvar_config, fg_color="#E6C8FA",
                                         dropdown_fg_color="#654E82", text_color="black", button_color="#E6C8FA")
        self.OptionMenu1.set(resolucao_sel)
        self.OptionMenu1.place(relx=0.43, rely=0.3, anchor=W, relwidth=0.18, relheight=0.1)

        self.OptionMenu3 = CTkOptionMenu(frame2, values=["FPS","120 fps", "60 fps", "30 fps"],
                                         command=self.salvar_config, fg_color="#E6C8FA",
                                         dropdown_fg_color="#654E82", text_color="black", button_color="#E6C8FA")
        self.OptionMenu3.set(fps_sel)
        self.OptionMenu3.place(relx=0.63, rely=0.3, anchor=W, relwidth=0.18, relheight=0.1)

        self.OptionMenu2 = CTkOptionMenu(frame2, values=["Idiomas","português", "Inglês", "Espanhol"],
                                         command=self.salvar_config, fg_color="#E6C8FA",
                                         dropdown_fg_color="#654E82", text_color="black", button_color="#E6C8FA")
        self.OptionMenu2.set(idioma_sel)
        self.OptionMenu2.place(relx=0.23, rely=0.5, anchor=W, relwidth=0.58, relheight=0.1)

        # --- Labels ---
        camera = CTkLabel(frame2, text="Câmera", font=("Arial", 15), text_color="#E6C8FA")
        camera.place(relx=0.14, rely=0.26, anchor=W)

        lingua = CTkLabel(frame2, text="Língua", font=("Arial", 15), text_color="#E6C8FA")
        lingua.place(relx=0.14, rely=0.46, anchor=W)

        termos_de_uso = CTkLabel(frame2, text="Termos de Uso", font=("Arial", 15), text_color="#E6C8FA", cursor="hand2")
        termos_de_uso.place(relx=0.15, rely=0.9, anchor=CENTER)
        termos_de_uso.bind("<Button-1>", lambda e: self.controller.mostrar_pagina("termos_de_uso"))

        # --- Label que mostra as configurações atuais ---
        self.info_label = CTkLabel(self, text="", font=("Arial", 14), text_color="white", bg_color="transparent")
        self.info_label.place(relx=0.5, rely=0.9, anchor=CENTER)
        self.atualizar_info_label()  # mostra o estado inicial

        # --- Botões de navegação ---
        icone_voltar = CTkImage(Image.open("assets/ImgsTemp/seta_esquerda.png"), size=(20, 20))
        icone_avanc = CTkImage(Image.open("assets/ImgsTemp/seta_direita.png"), size=(20, 20))

        btn_voltar = CTkButton(self, image=icone_voltar, text="", fg_color="#654E82",
                               command=lambda: controller.mostrar_pagina("config"))
        btn_voltar.place(relx=0.07, rely=0.15, anchor=CENTER, relwidth=0.05, relheight=0.06)

        avanc = CTkButton(self, image=icone_avanc, text="", fg_color="#654E82",
                          command=lambda: controller.mostrar_pagina("inicial"))
        avanc.place(relx=0.9, rely=0.15, anchor=CENTER, relwidth=0.05, relheight=0.06)

    # --- Salva e atualiza o texto ---
    def salvar_config(self, _=None):
        salvar_ajustes(
            self.OptionMenu1.get(),
            self.OptionMenu2.get(),
            self.OptionMenu3.get(),
            self.OptionMenu5.get()
        )
        self.atualizar_info_label()

    # --- Atualiza o label de informações ---
    def atualizar_info_label(self):
        dados = carregar_ajustes()
        if dados:
            resolucao, idioma, fps, luz = dados
            self.info_label.configure(
                text=f"📋 Configurações atuais:\nResolução: {resolucao} | Idioma: {idioma} | FPS: {fps} | Luz da Câmera: {luz}"
            )
        else:
            self.info_label.configure(text="Nenhuma configuração salva ainda.")
