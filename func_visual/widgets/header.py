from customtkinter import CTkFrame, CTkLabel, CENTER, CTkButton, CTkImage
from PIL import Image

def nav(self, controller, texto, logo_path=None):
    # Header principal
    header = CTkFrame(self, fg_color="#654E82", corner_radius=0)
    header.place(relx=0, rely=0, relwidth=1, relheight=0.1)
    
    image = CTkImage(Image.open("assets/Logos/NovaLogo.png"), size=(100, 90))
    logo_label = CTkLabel(header, image=image, text="")
    logo_label.place(relx=0.05, rely=0.5, anchor=CENTER)

    # Título ao lado da logo
    titulo = CTkLabel(header, text=texto, font=("Bold", 20), text_color="#E6C8FA")
    titulo.place(relx=0.15, rely=0.5, anchor=CENTER) 

    # Botão de fechar
    close = CTkButton(header, text="X", font=("Bold", 20), text_color="#E6C8FA", 
                      command=controller.destroy, fg_color="#48365E", hover_color="#332346")
    close.place(relx=0.95, rely=0.5, anchor=CENTER, relwidth=0.05, relheight=0.5)
