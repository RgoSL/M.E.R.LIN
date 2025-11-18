from customtkinter import get_appearance_mode, set_appearance_mode


def alternar_modo():
    modo_atual = get_appearance_mode()

    if modo_atual == "Light":
        set_appearance_mode("Dark")
    else:
        set_appearance_mode("Light")
