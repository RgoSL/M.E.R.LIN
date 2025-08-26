from customtkinter import *
from PIL import Image


def criar_containers(parent, variavel, opcoes=None, largura=400, altura=60):
    """
    Cria vários containers com base em um dicionário.
    Cada container tem tamanho fixo e layout com grid.
    
    :param parent: Frame ou janela onde os containers serão criados
    :param variavel: StringVar para armazenar a seleção
    :param opcoes: Dicionário opcional no formato {"chave": {"texto": str, "icone": caminho}}
    :param largura: largura do frame
    :param altura: altura do frame
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
        # Frame do container com tamanho fixo
        frame = CTkFrame(parent, corner_radius=10, fg_color="#FFFFFF", width=largura, height=altura, border_color="#C58ADE", border_width=2)
        frame.grid(row=i, column=0, padx=110, pady=10)
        frame.grid_propagate(False)  # impede que o conteúdo altere o tamanho

        # Configura colunas do grid para posicionar componentes
        frame.grid_columnconfigure(1, weight=1)  # coluna do texto expande

        # Ícone
        try:
            img = CTkImage(dark_image=Image.open(dados["icone"]), size=(28, 28))
            CTkLabel(frame, image=img, text="").grid(row=0, column=0, padx=10, pady=10)
        except:
            CTkLabel(frame, text="❓").grid(row=0, column=0, padx=10, pady=10)

        # Texto (expande para empurrar o botão para a direita)
        CTkLabel(frame, text=dados["texto"], anchor="w", font=("Bold", 16)).grid(row=0, column=1, padx=10, sticky="w")

        # Botão de seleção no final direito do container
        CTkRadioButton(
            frame,
            text="",
            value=chave,
            variable=variavel
        ).grid(row=0, column=2, padx=10, sticky="e")
