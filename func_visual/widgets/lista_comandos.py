from customtkinter import *
from PIL import Image

def criar_containers(parent, variavel, apps, largura=400, altura=60, cor_texto="#000000"):
    """
    Cria containers para cada app da lista passada.
    
    :param parent: Frame ou janela onde os containers serão criados
    :param variavel: StringVar para armazenar a seleção
    :param apps: Lista de apps, cada app é um dict {"name": str, "command": str, "icon": str opcional}
    :param largura: largura do frame
    :param altura: altura do frame
    :param cor_texto: cor do texto das opções
    """
    for i, app in enumerate(apps):
        frame = CTkFrame(parent, corner_radius=10, fg_color="#FFFFFF",
                         width=largura, height=altura, border_color="#C58ADE", border_width=2)
        frame.grid(row=i, column=0, padx=100, pady=5)
        frame.grid_propagate(False)
        frame.grid_columnconfigure(1, weight=1)

        # Ícone, se existir
        if "icon" in app and app["icon"]:
            try:
                img = CTkImage(dark_image=Image.open(app["icon"]), size=(28, 28))
                CTkLabel(frame, image=img, text="").grid(row=0, column=0, padx=10, pady=10)
            except:
                CTkLabel(frame, text="❓").grid(row=0, column=0, padx=10, pady=10)
        else:
            CTkLabel(frame, text="❓").grid(row=0, column=0, padx=10, pady=10)

        # Nome do app
        CTkLabel(frame, text=app["name"], anchor="w", font=("Bold", 16), text_color=cor_texto)\
            .grid(row=0, column=1, padx=10, sticky="w")

        # RadioButton para seleção
        CTkRadioButton(frame, text="", value=app["name"], variable=variavel,
                       fg_color="#654E82").grid(row=0, column=2, padx=10, sticky="e")
