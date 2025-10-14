from customtkinter import CTkFrame, CTkLabel, CENTER,CTkButton

def nav(self, controller, texto):
    header = CTkFrame(self, fg_color="#654E82", corner_radius=0)
    header.place(relx=0, rely=0, relwidth=1, relheight=0.1)
    titulo = CTkLabel(header, text=texto, font=("Bold", 20), text_color="#E6C8FA")
    titulo.place(relx=0.1, rely=0.5, anchor=CENTER)
    close = CTkButton(header, text="X", font=("Bold", 20), text_color="#E6C8FA", command=controller.destroy, fg_color="red")
    close.place(relx=0.95, rely=0.5, anchor=CENTER, relwidth=0.05, relheight=0.5)