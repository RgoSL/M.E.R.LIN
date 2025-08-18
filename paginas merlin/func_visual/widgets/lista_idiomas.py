from customtkinter import CTkLabel

idiomas = {
    "pt": "Português",
    "en": "Inglês",
    "es": "Espanhol",
    "fr": "Francês",
    "de": "Alemão",
    "it": "Italiano",
    "ja": "Japonês",
    "zh": "Chinês",
}

def criar_lista_idiomas(frame, idiomas, padding_y=10):
    """
    Cria labels para cada idioma dentro do frame com espaçamento vertical (pady).

    :param frame: O frame onde os labels serão adicionados
    :param idiomas: Dicionário {codigo: nome}
    :param padding_y: Espaçamento vertical entre os labels
    :return: lista de labels criados
    """
    labels = []
    for codigo, nome in idiomas.items():
        label = CTkLabel(
            frame,
            text=f"{nome} ({codigo})",
            fg_color="#FFFFFF",
            text_color="black",
            corner_radius=5,
            anchor="w"  # texto alinhado à esquerda
        )
        label.pack(pady=(0, padding_y), anchor="w", padx=5)  # label alinhado à esquerda
        labels.append(label)
    return labels
