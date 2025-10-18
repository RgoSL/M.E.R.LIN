from customtkinter import *
from PIL import Image
import os
from func_visual.widgets.header import nav
class ajustes(CTkFrame):
    def __init__(self, master, controller):
            super().__init__(master)
            self.controller = controller

            nav(self,controller, "M.E.R.LIN")

            titulo = CTkLabel(self, text="Ajustes", font=("Bold", 20), text_color=None, bg_color="transparent")
            titulo.place(relx=0.5, rely=0.15, anchor=CENTER)

            frame2 = CTkFrame(self, fg_color="#654E82", corner_radius=15)
            frame2.place(relx=0.5, rely=0.6, relwidth=0.8, relheight=0.5, anchor=CENTER)

             # COMBOBOX CORRETO:
            self.combobox_var = StringVar(value="Opção 1")
        
            OptionMenu1 = CTkOptionMenu(frame2, values=["Resolução","1080p", "720p", "360p"], command=self.combobox_callback, width=200, fg_color="#E6C8FA", corner_radius=5, dropdown_fg_color="#654E82", button_color="#E6C8FA", button_hover_color="#E6C8FA", text_color="black")
            OptionMenu1.place(relx=0.59, rely=0.3, anchor=CENTER, relwidth=0.2, relheight=0.1)

            OptionMenu2 = CTkOptionMenu(frame2, values=["Idiomas","português", "Inglês", "Espanhol"], command=self.combobox_callback, width=200, fg_color="#E6C8FA", corner_radius=5, dropdown_fg_color="#654E82", button_color="#E6C8FA", button_hover_color="#E6C8FA", text_color="black")
            OptionMenu2.place(relx=0.56, rely=0.5, anchor=CENTER, relwidth=0.521, relheight=0.1)

            OptionMenu3 = CTkOptionMenu(frame2, values=["FPS","120 fps", "60 fps", "30 fps"], command=self.combobox_callback, width=200, fg_color="#E6C8FA", corner_radius=0, dropdown_fg_color="#654E82", button_color="#E6C8FA", button_hover_color="#E6C8FA", text_color="black")
            OptionMenu3.place(relx=0.714, rely=0.3, anchor=CENTER, relwidth=0.2, relheight=0.1)

            OptionMenu5 = CTkOptionMenu(frame2, values=["Luz da Camera","Sim", "Não"], command=self.combobox_callback, width=200, fg_color="#E6C8FA", corner_radius=0, dropdown_fg_color="#654E82", button_color="#E6C8FA", button_hover_color="#E6C8FA", text_color="black")
            OptionMenu5.place(relx=0.40, rely=0.3, anchor=CENTER, relwidth=0.2, relheight=0.1)

            camera = CTkLabel(frame2, text="Câmera", font=("Arial", 15), text_color="#E6C8FA")
            camera.place(relx=0.23, rely=0.26, anchor=CENTER)

            lingua = CTkLabel(frame2, text="Língua", font=("Arial", 15), text_color="#E6C8FA")
            lingua.place(relx=0.23, rely=0.46, anchor=CENTER)

            termos_de_uso = CTkLabel(frame2, text="Termos de Uso", font=("Arial", 15), text_color="#E6C8FA", cursor="hand2")
            termos_de_uso.place(relx=0.15, rely=0.9, anchor=CENTER)
            termos_de_uso.bind("<Button-1>", lambda e: self.controller.mostrar_pagina("termos_de_uso"))
          

            icone_voltar = CTkImage(Image.open("assets/ImgsTemp/seta_esquerda.png"), size=(20, 20))
            icone_avanc = CTkImage(Image.open("assets/ImgsTemp/seta_direita.png"), size=(20, 20))

            btn_voltar = CTkButton(self, image=icone_voltar, text="", text_color="#E6C8FA", fg_color="#654E82",command=lambda: controller.mostrar_pagina("config"))
            btn_voltar.place(relx=0.07, rely=0.15, anchor=CENTER, relwidth=0.05, relheight=0.06)

            avanc = CTkButton(self, image=icone_avanc, text="", text_color="#E6C8FA", fg_color="#654E82",command=lambda: controller.mostrar_pagina("inicial"))
            avanc.place(relx=0.9, rely=0.15, anchor=CENTER, relwidth=0.05, relheight=0.06)


    def combobox_callback(self, choice):  # ← self
        print(f"Selecionado: {choice}")