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

            frame2 = CTkFrame(frame, fg_color="#654E82", corner_radius=15)
            frame2.place(relx=0.5, rely=0.5, relwidth=0.8, relheight=0.7, anchor=CENTER)

             # COMBOBOX CORRETO:
            self.combobox_var = StringVar(value="Opção 1")
        
            combobox = CTkComboBox(frame2,values=["Opção 1", "Opção 2", "Opção 3"],command=self.combobox_callback,width=200, fg_color="#E6C8FA") # ← self.variable=self.combobox_var
            combobox.place(relx=0.55, rely=0.3, anchor=CENTER)
    
    def combobox_callback(self, choice):  # ← self
        print(f"Selecionado: {choice}")