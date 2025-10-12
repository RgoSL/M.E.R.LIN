from customtkinter import CTkProgressBar

def progress_bar(master, valor=0.0, modo="determinate",
                 cor_corpo="#654E82", cor_progresso="#C58ADE", 
                 cor_fundo="transparent", altura=20, largura=200):
    """
    Cria uma barra de progresso personalizada e garante que o valor apareça.
    """
    barra = CTkProgressBar(
        master,
        fg_color=cor_corpo,
        progress_color=cor_progresso,
        bg_color=cor_fundo,
        mode=modo,
        width=largura,
        height=altura
    )

    # Posicionar temporariamente para renderizar
    barra.place(x=-100, y=-100)  # fora da tela por enquanto
    barra.set(valor)              # define o progresso
    barra.place_forget()          # remove temporariamente
    return barra
