


from customtkinter import CTkLabel
import os

# Só idiomas necessários
idiomas = {
    "pt": "Português",
    "en": "Inglês",
    "es": "Espanhol",
}

# Lista de pares que queremos suportar
pares_disponiveis = [
    ("pt", "en"), ("en", "pt"),
    ("pt", "es"), ("es", "pt"),
    ("en", "es"), ("es", "en")
]

def criar_lista_idiomas(frame, idiomas, callback, padding_y=10):
    #Cria labels clicáveis de idiomas.
    labels = []
    for codigo, nome in idiomas.items():
        label = CTkLabel(
            frame,
            text=f"{nome} ({codigo})",
            fg_color="#FFFFFF",
            text_color="black",
            corner_radius=5,
            anchor="w"
        )
        label.bind("<Button-1>", lambda e, c=codigo: callback(c))
        label.pack(pady=(0, padding_y), anchor="w", padx=5)
        labels.append(label)
    return labels

