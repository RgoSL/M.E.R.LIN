# Bibliotecas Utilizadas 
from customtkinter import *
from PIL import Image

# Função de Criação da Classe Dessa Tela
class configSo(CTkFrame):
    def __init__(self, master, controller=None):
        super().__init__(master)
        self.controller = controller

        # Frame Para Agrupar os SO
        self.Container_Sis = CTkFrame(self, fg_color="#654E82", border_color="#000000", border_width=2)
        self.Container_Sis.place(relx=0.5, rely=0.5, anchor="center")  # Centralizado na tela

        # Caminho de Cada Imagem de Sistema
        caminho_win = r"D:/CÓDIGOS/ETEC/TCC/paginas merlin/assets/ImgsSo/IconWin.png" 
        caminho_lin = r"D:/CÓDIGOS/ETEC/TCC/paginas merlin/assets/ImgsSo/IconLin.png"
        caminho_mac = r"D:/CÓDIGOS/ETEC/TCC/paginas merlin/assets/ImgsSo/IconMac.png"

        # Padronização das Imagens
        tamanho_icones = (150, 150)

        # Carregamento das imagens
        self.img_windows = self.ImgSis(caminho_win, tamanho_icones)
        self.img_linux = self.ImgSis(caminho_lin, tamanho_icones)
        self.img_mac = self.ImgSis(caminho_mac, tamanho_icones)

        # Frame Onde Estão Posicionados Cada SO
        self.grid_frame = CTkFrame(self.Container_Sis, fg_color="transparent")
        self.grid_frame.pack(padx=20, pady=20)

        # Cards Para Cada Sistema
        self.criar_card_so(self.grid_frame, self.img_windows, "Windows", 0, self.on_click_windows)
        self.criar_card_so(self.grid_frame, self.img_linux, "Linux", 1, self.on_click_linux)
        self.criar_card_so(self.grid_frame, self.img_mac, "macOS", 2, self.on_click_mac)

    # Função Para Padronizar as Imagens
    def ImgSis(self, src: str, tam: tuple = (100, 100)) -> CTkImage:
        img = Image.open(src)
        img_resized = img.resize(tam, Image.Resampling.LANCZOS)
        return CTkImage(light_image=img_resized, dark_image=img_resized, size=tam)

    def criar_card_so(self, master, imagem, nome, coluna, comando):
        frame = CTkFrame(master, fg_color="transparent")
        frame.grid(row=0, column=coluna, padx=40, pady=10)

        # Função Para Tornar as Imagens Clicáveis
        btn = CTkButton(frame, image=imagem, text="", width=150, height=150,
                        fg_color="transparent", hover_color="#4b3b5f", command=comando)
        btn.pack()

        label = CTkLabel(frame, text=nome, text_color="white")
        label.pack(pady=5)

    # Funções Temporárias Para Testar Cada Imagem
    def on_click_windows(self):
        print("Windows Funfa.")

    def on_click_linux(self):
        print("Linux funfa")

    def on_click_mac(self):
        print("MacOS funfa")


# Execução Local e Temporária Dessa Classe
if __name__ == "__main__":
    set_appearance_mode("dark")
    set_default_color_theme("blue")

    app = CTk()
    app.geometry("900x600")
    app.title("Tela de Configuração de Sistema")

    tela_config = configSo(master=app)
    tela_config.pack(fill="both", expand=True)

    app.mainloop()
