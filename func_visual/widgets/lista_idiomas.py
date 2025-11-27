from customtkinter import CTkLabel

from func_visual.widgets.i18n import i18n

idiomas = { # Idiomas Está Ligado as Chaves do Dicionário na Classe i18
    "pt": "pt", 
    "en": "en",
    "es": "es",
    "ar": "ar",
}

pares_disponiveis = [
    ("pt", "en"),
    ("en", "pt"),
    ("pt", "es"),
    ("es", "pt"),
    ("en", "es"),
    ("es", "en"),
    ("ar", "en"),
    ("en", "ar"),
    ("ar", "pt"),
    ("pt", "ar"),
    ("es", "ar"),
    ("ar", "es"),
]

# Função Para Criar a Lista Exibida na Tela de Idiomas
def criar_lista_idiomas(frame, idiomas_dict, callback, padding_y=10):
    labels = []
    
    # Nomes da Lista Agora Valem as Chaves do Dicionário
    nomes_idiomas = {
        "pt": "portugues",
        "en": "ingles",
        "es": "espanhol",
        "ar": "arabe"
    }
    
    for codigo in idiomas_dict.keys():
        # Laço Para Traduzir Somente o Nome do Idioma em Outra Lingua
        nome_traduzido = i18n.t(nomes_idiomas.get(codigo, codigo))
        
        label = CTkLabel(
            frame,
            text=f"{nome_traduzido} ({codigo.upper()})",
            fg_color="#FFFFFF",
            text_color="black",
            corner_radius=5,
            anchor="w",
            cursor="hand2" 
        )
        
        # Callback é um Parâmetro Para Acionar a Funcionalidade da Troca de Idiomas
        if callback:
            label.bind("<Button-1>", lambda e, c=codigo: callback(c))
        
        label.pack(pady=(0, padding_y), anchor="w", padx=5, fill="x")
        labels.append((codigo, label))
    
    return labels