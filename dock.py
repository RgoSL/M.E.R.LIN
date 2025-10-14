from customtkinter import *
from PIL import Image
from comandos_dock import btns
from lista_apps import abrir_lista_apps
import os

# ===================== Inicialização =====================
Dock = CTk()
Dock.title("Dock")
Dock.update_idletasks()  # garante que a janela esteja pronta

# Ícone para que apareça na taskbar
icon_path = os.path.join("images", "icone.ico")
if os.path.exists(icon_path):
    Dock.iconbitmap(icon_path)

# ===================== Aparência e atributos =====================
Dock.overrideredirect(True)  # remove borda nativa
Dock.attributes("-topmost", True)
Dock.attributes("-toolwindow", False)  # evita tratar como janela de ferramenta
Dock.wm_attributes("-transparentcolor", "#654E82")  # cor transparente

# ===================== Posicionamento =====================
altura_tela = Dock.winfo_screenheight()
largura_tela = Dock.winfo_screenwidth()
largura_dock = 80
altura_dock = 370
dock_x = largura_tela - largura_dock
dock_y = altura_tela // 3
Dock.geometry(f"{largura_dock}x{altura_dock}+{dock_x}+{dock_y}")

# ===================== Frame principal =====================
Frame = CTkFrame(
    Dock, fg_color="#644C81", border_width=1, border_color="#f9b14f", corner_radius=10
)
Frame.pack(fill="both", expand=True)

# ===================== Função de criação de botões =====================
def btns_dock(caminho, command=None):
    imagem = Image.open(caminho).resize((60, 60))
    ctk_img = CTkImage(light_image=imagem, dark_image=imagem)
    
    bot = CTkButton(
        Frame,
        image=ctk_img,
        text="",
        width=60,
        height=60,
        fg_color="#432D5D",
        hover_color="#C58ADE",
        corner_radius=10,
        command=command
    )
    bot.image = ctk_img
    bot.pack(pady=8)
    return bot

# ===================== Botões da Dock =====================
btns_dock("images/ImgsDock/LApps.png", command=lambda: abrir_lista_apps(Dock))
btns_dock("images/ImgsDock/pacotes.png", command=lambda: btns.Btn_Pacotes())
btns_dock("images/ImgsDock/navegador.png", command=lambda: btns.Btn_Navegador())
btns_dock("images/ImgsDock/Fechar.png", command=Dock.destroy)

# ===================== Função de manter janela ativa =====================
def manter_aberta():
    """Evita que o Windows feche a janela por falta de foco."""
    if not Dock.winfo_exists():
        return  # se fechou, não faz nada
    Dock.after(1000, manter_aberta)

manter_aberta()

# ===================== Mainloop =====================
Dock.mainloop()
