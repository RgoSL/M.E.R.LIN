from customtkinter import *
from PIL import Image
import os



class ajustes(CTkFrame):
    def __init__(self, master, controller):
            super().__init__(master)
            self.controller = controller

            frame = CTkFrame(self, fg_color="#FFFFFF", corner_radius=0)
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)

            header = CTkFrame(frame, fg_color="#654E82", corner_radius=0)
            header.place(relx=0, rely=0, relwidth=1, relheight=0.1)

            titulo = CTkLabel(header, text="Ajustes", font=("Bold", 20), text_color="black")
            titulo.place(relx=0.5, rely=0.5, anchor=CENTER)

            txt_logo = CTkLabel(header, text="M.E.R.LIN", font=("Bold", 20), text_color="#E6C8FA")
            txt_logo.place(relx=0.1, rely=0.5, anchor=CENTER)

            frame2 = CTkFrame(frame, fg_color="#654E82", corner_radius=15)
            frame2.place(relx=0.5, rely=0.55, relwidth=0.8, relheight=0.7, anchor=CENTER)


            

             # COMBOBOX CORRETO:
            self.combobox_var = StringVar(value="Opção 1")
        
            OptionMenu1 = CTkOptionMenu(frame2, values=["Resolução","1080p", "720p", "360p"], command=self.combobox_callback, width=200, fg_color="#E6C8FA", corner_radius=5, dropdown_fg_color="#E6C8FA", button_color="#E6C8FA", button_hover_color="#E6C8FA", text_color="black")
            OptionMenu1.place(relx=0.59, rely=0.3, anchor=CENTER, relwidth=0.2, relheight=0.1)

            OptionMenu2 = CTkOptionMenu(frame2, values=["Opção A", "Opção B", "Opção C"], command=self.combobox_callback, width=200, fg_color="#E6C8FA", corner_radius=5, dropdown_fg_color="#E6C8FA", button_color="#E6C8FA", button_hover_color="#E6C8FA", text_color="black")
            OptionMenu2.place(relx=0.59, rely=0.5, anchor=CENTER, relwidth=0.2, relheight=0.1)

            OptionMenu3 = CTkOptionMenu(frame2, values=["FPS","120 fps", "60 fps", "30 fps"], command=self.combobox_callback, width=200, fg_color="#E6C8FA", corner_radius=0, dropdown_fg_color="#E6C8FA", button_color="#E6C8FA", button_hover_color="#E6C8FA", text_color="black")
            OptionMenu3.place(relx=0.714, rely=0.3, anchor=CENTER, relwidth=0.2, relheight=0.1)

            OptionMenu4 = CTkOptionMenu(frame2, values=["Seleção 1", "Seleção 2", "Seleção 3"], command=self.combobox_callback, width=200, fg_color="#E6C8FA", corner_radius=0, dropdown_fg_color="#E6C8FA", button_color="#E6C8FA", button_hover_color="#E6C8FA", text_color="black")
            OptionMenu4.place(relx=0.714, rely=0.5, anchor=CENTER, relwidth=0.2, relheight=0.1)

            OptionMenu5 = CTkOptionMenu(frame2, values=["Luz da Camera","Sim", "Não"], command=self.combobox_callback, width=200, fg_color="#E6C8FA", corner_radius=0, dropdown_fg_color="#E6C8FA", button_color="#E6C8FA", button_hover_color="#E6C8FA", text_color="black")
            OptionMenu5.place(relx=0.40, rely=0.3, anchor=CENTER, relwidth=0.2, relheight=0.1)

            OptionMenu6 = CTkOptionMenu(frame2, values=["Config 1", "Config 2", "Config 3"], command=self.combobox_callback, width=200, fg_color="#E6C8FA", corner_radius=0, dropdown_fg_color="#E6C8FA", button_color="#E6C8FA", button_hover_color="#E6C8FA", text_color="black")
            OptionMenu6.place(relx=0.40, rely=0.5, anchor=CENTER, relwidth=0.2, relheight=0.1)

            camera = CTkLabel(frame2, text="Câmera", font=("Arial", 15), text_color="#E6C8FA")
            camera.place(relx=0.23, rely=0.26, anchor=CENTER)

            lingua = CTkLabel(frame2, text="Língua", font=("Arial", 15), text_color="#E6C8FA")
            lingua.place(relx=0.23, rely=0.46, anchor=CENTER)

            termos_de_uso = CTkLabel(frame2, text="Termos de Uso", font=("Arial", 15), text_color="#E6C8FA")
            termos_de_uso.place(relx=0.15, rely=0.9, anchor=CENTER)

            icone_voltar = CTkImage(Image.open("images/seta_esquerda.png"), size=(20, 20))

            btn_voltar = CTkButton(frame, image=icone_voltar, text="", text_color="#E6C8FA", fg_color="#654E82", command=lambda: controller.mostrar_pagina("config"))
            btn_voltar.place(relx=0.07, rely=0.15, anchor=CENTER, relwidth=0.05, relheight=0.06)


    def combobox_callback(self, choice):  # ← self
        print(f"Selecionado: {choice}")