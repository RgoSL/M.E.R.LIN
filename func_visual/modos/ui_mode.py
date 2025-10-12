from customtkinter import set_appearance_mode,get_appearance_mode

def alternar_modo():
    """Alterna entre modo claro e escuro."""
    # Pega o modo atual
    modo_atual = get_appearance_mode()
    
    # Alterna
    if modo_atual == "Light":
        set_appearance_mode("Dark")
    else:
        set_appearance_mode("Light")