from customtkinter import CTkProgressBar


def progress_bar(
    master,
    valor=0.0,
    modo="determinate",
    cor_corpo="#654E82",
    cor_progresso="#C58ADE",
    cor_fundo="transparent",
    altura=20,
    largura=200,
):

    barra = CTkProgressBar(
        master,
        fg_color=cor_corpo,
        progress_color=cor_progresso,
        bg_color=cor_fundo,
        mode=modo,
        width=largura,
        height=altura,
    )

    barra.place(x=-100, y=-100)
    barra.set(valor)
    barra.place_forget()
    return barra
