from customtkinter import CTkFrame, CTkLabel, CTkButton

# Definindo paletas
PALETA_CLARA = {
    "bg": "#FFFFFF",
    "fg": "#000000",
    "header": "#654E82",
    "texto_header": "#E6C8FA",
    "botao": "#654E82",
    "texto_botao": "#FFFFFF",
    "progresso": "#C58ADE"
}

PALETA_ESCURO = {
    "bg": "#2B2B2B",
    "fg": "#FFFFFF",
    "header": "#1F1F1F",
    "texto_header": "#E6C8FA",
    "botao": "#3A3A3A",
    "texto_botao": "#FFFFFF",
    "progresso": "#9C5CC1"
}


def aplicar_tema(frame, paleta):
    """Aplica as cores do tema em todos os widgets dentro do frame"""
    frame.configure(fg_color=paleta["bg"])

    for widget in frame.winfo_children():
        if isinstance(widget, CTkFrame):
            widget.configure(fg_color=paleta["header"])
        elif isinstance(widget, CTkLabel):
            widget.configure(text_color=paleta["fg"])
        elif isinstance(widget, CTkButton):
            widget.configure(fg_color=paleta["botao"], text_color=paleta["texto_botao"])

        # chamada recursiva para atualizar filhos
        aplicar_tema(widget, paleta)


def tema_claro(frame):
    aplicar_tema(frame, PALETA_CLARA)


def tema_escuro(frame):
    aplicar_tema(frame, PALETA_ESCURO)
