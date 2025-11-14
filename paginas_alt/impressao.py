# Classe da Primeira Tela ao Iniciar o Software

# Import das Bibliotecas Utilizadas na Construção da Tela
from PIL import Image, ImageDraw, ImageFont, ImageTk  # Biblioteca de Aplicação de Imagens e Fontes Customizadas
from customtkinter import *  # Biblioteca de Desenvolvimento de GUIs
import os # Biblioteca de Interação com Funções Base da Máquina do Usuário

# Import de Outras Classes do Software
from func_visual.widgets.header import nav  # Import do Header Padrão do Sistema

class bemVindo(CTk):
    def __init__(self, master, controller=None):
        super().__init__(master)
        self.controller = controller
        self.title("Bem-Vindo")
        self.geometry("600x800") 

        nav(self, controller, "M.E.R.LIN")  

        self.label_titulo = CTkLabel(self, text="Bem-Vindo ao Mundo Mágico", font=("GideonRoman-Regular", 24), text_color="#654E82")
        self.label_titulo.place(relx=0.5, rely=0.15, anchor="center")

        BASE_DIR = os.path.dirname(os.path.dirname(__file__))
        caminho_imagem = os.path.join(BASE_DIR, "assets", "ImgsSo", "IconWin.png")  

        img = Image.open(caminho_imagem)
        img_resized = img.resize((200, 200), Image.Resampling.LANCZOS)
        self.img_titulo = CTkImage(light_image=img_resized, dark_image=img_resized, size=(200, 200))

        self.img_label = CTkLabel(self, image=self.img_titulo, text="")
        self.img_label.place(relx=0.5, rely=0.35, anchor="center")

        self.label_texto = CTkLabel(self, text="Prepare-se para explorar novas possibilidades\ncom magia e estilo.", font=("GideonRoman-Regular", 18), text_color="#000000")
        self.label_texto.place(relx=0.5, rely=0.55, anchor="center")

        self.botao_comecar = CTkButton(
            self, text="Começar", text_color="#FFFFFF", fg_color="#654E82",
            font=("Bold", 16), bg_color="transparent", corner_radius=10,
            height=50, width=200, hover_color="#56397C", command=self.iniciar_app
        )
        self.botao_comecar.place(relx=0.5, rely=0.75, anchor="center")