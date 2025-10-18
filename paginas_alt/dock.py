# Import das Bibliotecas Utilizadas
from customtkinter import *
from PIL import Image

# Import das Classes com as Funcionalidades da Dock
from func_nao_visual.lista_apps import abrir_lista_apps
from func_nao_visual.comandos_dock import btns

Dock = CTk() 

# Posicionamento da Dock
Dock.overrideredirect(True)
Dock.attributes("-topmost", True)
Dock.wm_attributes("-transparentcolor", "#654E82") 

# Posicionamento da Dock na Tela
altura_tela = Dock.winfo_screenheight()
largura_tela = Dock.winfo_screenwidth()
largura_dock = 80
altura_dock = 370
dock_x = largura_tela - largura_dock
dock_y = altura_tela/3
Dock.geometry(f"{largura_dock} x {altura_dock} + {dock_x} + {int(dock_y)}")

# Container Principal
Frame = CTkFrame(Dock, bg_color="#654E82", fg_color = "#644C81", border_width = 1, border_color = "#f9b14f", corner_radius = 10)
Frame.pack(fill="both", expand=True)

# Definição do Formato dos Botões da Dock
def btns_dock(caminho, command = None):
    Btn = Image.open(caminho)
    Btn = Btn.resize((150, 120))
    Btn = CTkImage(light_image = Btn, dark_image = Btn)
    
# Formato de Botão dos Icones da Dock
    Bot = CTkButton(
        Frame,
        image = Btn,
        text = "",
        width = 60,
        height = 60,
        fg_color = "#432D5D",
        hover_color = "#C58ADE",
        corner_radius = 10,
        command = command
    )
    Bot.image = Btn
    Bot.pack(pady = 8)
    return Bot

# Botões da Dock, Funcionalidade de Cada um Sendo Ativada por uma Lambda
btns_dock("assets/ImgsDock/LApps.png", command=lambda: abrir_lista_apps(Dock))
btns_dock("assets/ImgsDock/pacotes.png", command=lambda: btns.Btn_Pacotes())
btns_dock("assets/ImgsDock/navegador.png", command=lambda: btns.Btn_Navegador())
btns_dock("assets/ImgsDock/Fechar.png", command=lambda: btns.Btn_Fechar(Dock))

Dock.mainloop()