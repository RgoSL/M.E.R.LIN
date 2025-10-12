# Dock com 3 Botões : Lista de Aplicativos, Abrir Pacote de Comandos, Abrir Pacote de Comandos II

from comandos_dock import *
from customtkinter import *
from PIL import Image

Dock = CTk() 

# Posicionamento da Dock
Dock.overrideredirect(True)
Dock.attributes("-topmost", True)
altura_tela = Dock.winfo_screenheight()
largura_tela = Dock.winfo_screenwidth()
largura_dock = 80
altura_dock = 370
dock_x = largura_tela - largura_dock
dock_y = altura_tela/3
Dock.geometry(f"{largura_dock}x{altura_dock}+{dock_x}+{dock_y}")

# Container Principal
Frame = CTkFrame(Dock, fg_color = "#654E82", border_width = 1 , border_color = "#f9b14f", corner_radius = 10)
Frame.pack(fill = "both", expand = True)

def btns_dock(caminho, command = None): # Função de Adição de Botão
    Btn = Image.open(caminho)
    Btn = Btn.resize((150, 120))
    Btn = CTkImage(light_image = Btn, dark_image = Btn)
    
    Bot = CTkButton ( # Container de Cada Botão
        Frame, image = Btn, text = "", width = 60, height = 60, fg_color = "#432D5D", hover_color = "#C58ADE", corner_radius = 10, command = command
    )
    Bot.image = Btn
    Bot.pack(pady = 8)
    return Bot

# Botões da Dock
btns_dock("images\ImgsDock/LApps.png", lambda: Btn_Lista)
btns_dock("images\ImgsDock/pacotes.png", lambda: Btn_Pacotes) 
btns_dock("images\ImgsDock/pacotes.png", lambda: Btn_Pacotes)
btns_dock("images\ImgsDock/navegador.png", lambda: Btn_Navegador) 
btns_dock("images\ImgsDock/Fechar.png",)


Dock.mainloop() 