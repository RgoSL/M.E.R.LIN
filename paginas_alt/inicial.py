from customtkinter import *
from func_nao_visual.mouse_scroll import mouse_scroll
from func_visual.funcs_imgs.img_redonda import configurar_imagens_no_frame
from func_visual.widgets.header import nav
from PIL import Image


class inicial(CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        nav(self, controller, "M.E.R.LIN")

        Titulo = CTkLabel(
            self,
            text="Seus Feitiços",
            font=("Gideon Roman", 30, "bold"),
            text_color="#654E82",
            anchor="center",
            justify="center",
        )
        Titulo.place(relx=0.5, rely=0.2, anchor=CENTER)

        frame1 = CTkScrollableFrame(
            self,
            fg_color="#654E82",
            corner_radius=15,
            orientation="horizontal",
            scrollbar_button_color="#F9B14F",
            scrollbar_button_hover_color="#F9B14F",
        )
        frame1.place(relx=0.5, rely=0.6, relwidth=0.8, relheight=0.5, anchor=CENTER)

        finalizar = CTkButton(
            self,
            text="Finalizar",
            fg_color="#654E82",
            bg_color="transparent",
            font=("Gideon Roman", 20, "bold"),
            hover_color="#56397C",
            command=self.closeOpenDock,
        )
        finalizar.place(
            relx=0.5, rely=0.93, anchor="center", relwidth=0.3, relheight=0.09
        )
        content_frame = CTkFrame(frame1, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)

        icone_voltar = CTkImage(
            Image.open("assets/ImgsTemp/seta_esquerda.png"), size=(20, 20)
        )

        btntst = CTkButton(
            self,
            image=icone_voltar,
            text="",
            fg_color="#654E82",
            hover_color="#56397C",
            command=lambda: self.controller.mostrar_pagina("ajustes"),
        )
        btntst.place(
            relx=0.07, rely=0.15, anchor="center", relwidth=0.05, relheight=0.06
        )

        images_frame = CTkFrame(frame1, fg_color="transparent")
        images_frame.pack(expand=True, fill="both")

        images_frame.grid_columnconfigure(0, weight=1)
        images_frame.grid_columnconfigure(1, weight=1)
        images_frame.grid_rowconfigure(0, weight=1)

        mouse_scroll(frame1)
        configurar_imagens_no_frame(frame1, self.controller)

    def closeOpenDock(self):
        self.controller.withdraw()

        from paginas_alt.dock import Dock

        Dock(self.controller, self.controller)
