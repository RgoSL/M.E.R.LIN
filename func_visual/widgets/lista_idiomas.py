from customtkinter import CTkLabel
import argostranslate.package
import argostranslate.translate

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

def criar_lista_idiomas(frame, idiomas, callback, padding_y=10):
    """
    Cria labels clicáveis de idiomas.
    """
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

        # 🖱️ Clique altera idioma
        label.bind("<Button-1>", lambda e, c=codigo: callback(c))

        label.pack(pady=(0, padding_y), anchor="w", padx=5)
        labels.append(label)
    return labels
def instalar_modelos():
    argostranslate.package.update_package_index()
    packages = argostranslate.package.get_available_packages()
    pares = [
        ("en", "pt"), ("pt", "en"), ("pt", "es"), ("es", "pt"),
        ("pt", "fr"), ("fr", "pt"), ("pt", "de"), ("de", "pt"),
        ("pt", "it"), ("it", "pt"), ("pt", "ja"), ("ja", "pt"),
        ("pt", "zh"), ("zh", "pt")
    ]
    for de, para in pares:
        try:
            pacote = next(p for p in packages if p.from_code == de and p.to_code == para)
            caminho = pacote.download()
            argostranslate.package.install_from_path(caminho)
        except StopIteration:
            pass  # ignora pares não disponíveis
def traduzir_texto(texto, de="pt", para="en"):
    try:
        # Carrega os idiomas instalados
        idiomas = argostranslate.translate.get_installed_languages()

        # Busca o idioma de origem e destino
        idioma_origem = next((i for i in idiomas if i.code == de), None)
        idioma_destino = next((i for i in idiomas if i.code == para), None)

        # Se ambos existirem, traduz
        if idioma_origem and idioma_destino:
            traducao = idioma_origem.get_translation(idioma_destino)
            return traducao.translate(texto)
        else:
            print(f"Idiomas não encontrados: {de} -> {para}")
            return texto

    except Exception as e:
        print(f"Erro ao traduzir: {e}")
        return texto

    

