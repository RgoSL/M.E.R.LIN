from customtkinter import *
from PIL import Image


def criar_containers(parent, variavel, opcoes=None, largura=400, altura=60, cor_texto="#000000"):
    """
    Cria vários containers com base em um dicionário.
    Cada container tem tamanho fixo e layout com grid.
    
    :param parent: Frame ou janela onde os containers serão criados
    :param variavel: StringVar para armazenar a seleção
    :param opcoes: Dicionário opcional no formato {"chave": {"texto": str, "icone": caminho}}
    :param largura: largura do frame
    :param altura: altura do frame
    :param cor_texto: cor do texto das opções
    """
    if opcoes is None:
        opcoes = {
            "config": {"texto": "Configurações", "icone": "images/logoicon.ico"},
            "ajustes": {"texto": "Ajustes", "icone": "images/logoicon.ico"},
            "video": {"texto": "Assistente de Vídeo", "icone": "images/logoicon.ico"},
            "imagem": {"texto": "Help", "icone": "images/logoicon.ico"},
            "bloco de notas": {"texto": "Teste", "icone": "images/logoicon.ico"},
        }

    for i, (chave, dados) in enumerate(opcoes.items()):
        frame = CTkFrame(parent, corner_radius=10, fg_color="#FFFFFF", width=largura, height=altura, border_color="#C58ADE", border_width=2)
        frame.grid(row=i, column=0, padx=110, pady=10)
        frame.grid_propagate(False)

        frame.grid_columnconfigure(1, weight=1)

        # Ícone
        try:
            img = CTkImage(dark_image=Image.open(dados["icone"]), size=(28, 28))
            CTkLabel(frame, image=img, text="").grid(row=0, column=0, padx=10, pady=10)
        except:
            CTkLabel(frame, text="❓").grid(row=0, column=0, padx=10, pady=10)

        # Texto com cor definida
        CTkLabel(frame, text=dados["texto"], anchor="w", font=("Bold", 16), text_color=cor_texto).grid(row=0, column=1, padx=10, sticky="w")

        CTkRadioButton(
            frame,
            text="",
            value=chave,
            variable=variavel,
            fg_color="#654E82",
        ).grid(row=0, column=2, padx=10, sticky="e")
