from customtkinter import *
from func_nao_visual.mouse_scroll import mouse_scroll
from func_visual.funcs_imgs.img_redonda import configurar_imagens_no_frame, atualizar_textos_imagens
from func_visual.widgets.header import nav
from func_visual.widgets.i18n import i18n
from PIL import Image

class inicial(CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        nav(self, controller, "M.E.R.LIN")

        self.titulo = CTkLabel(
            self,
            text=i18n.t("titulo_inicial"),
            font=("Gideon Roman", 30, "bold"),
            text_color="#654E82",
            anchor="center",
            justify="center",
        )
        self.titulo.place(relx=0.5, rely=0.2, anchor=CENTER)

        self.frame1 = CTkScrollableFrame(
            self,
            fg_color="#654E82",
            corner_radius=15,
            orientation="horizontal",
            scrollbar_button_color="#F9B14F",
            scrollbar_button_hover_color="#F9B14F",
        )
        self.frame1.place(relx=0.5, rely=0.6, relwidth=0.8, relheight=0.5, anchor=CENTER)

        self.btn_finalizar = CTkButton(
            self,
            text=i18n.t("finalizar"),
            fg_color="#654E82",
            bg_color="transparent",
            font=("Gideon Roman", 20, "bold"),
            hover_color="#56397C",
            command=self.closeOpenDock,
        )
        self.btn_finalizar.place(
            relx=0.5, rely=0.93, anchor="center", relwidth=0.3, relheight=0.09
        )

        content_frame = CTkFrame(self.frame1, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)

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

        images_frame = CTkFrame(self.frame1, fg_color="transparent")
        images_frame.pack(expand=True, fill="both")

        images_frame.grid_columnconfigure(0, weight=1)
        images_frame.grid_columnconfigure(1, weight=1)
        images_frame.grid_rowconfigure(0, weight=1)

        mouse_scroll(self.frame1)

        self.container_imagens = configurar_imagens_no_frame(self.frame1, self.controller)

    def atualizar_idioma(self):

        self.titulo.configure(text=i18n.t("titulo_inicial"))
        
        self.btn_finalizar.configure(text=i18n.t("finalizar"))
        
        if hasattr(self, 'container_imagens'):
            atualizar_textos_imagens(self.container_imagens)
        
        print(f"Página inicial atualizada para idioma: {i18n.idioma_atual}")

    def closeOpenDock(self):
        self.controller.withdraw()

        from paginas_alt.dock import Dock

        Dock(self.controller, self.controller)