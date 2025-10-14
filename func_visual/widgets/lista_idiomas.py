from customtkinter import CTkLabel
import argostranslate.package
import argostranslate.translate
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
    """Cria labels clicáveis de idiomas."""
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

def baixar_modelo(de, para):
    """Baixa e instala o modelo se não estiver instalado."""
    # Atualiza lista de pacotes disponíveis
    argostranslate.package.update_package_index()
    packages = argostranslate.package.get_available_packages()
    
    # Verifica se já está instalado
    idiomas_instalados = argostranslate.translate.get_installed_languages()
    if any(i.code == de for i in idiomas_instalados) and any(i.code == para for i in idiomas_instalados):
        # Modelo já instalado
        return

    # Tenta baixar
    try:
        pacote = next(p for p in packages if p.from_code == de and p.to_code == para)
        caminho = pacote.download()
        argostranslate.package.install_from_path(caminho)
        print(f"Modelo {de} -> {para} instalado com sucesso.")
    except StopIteration:
        print(f"Modelo {de} -> {para} não encontrado.")

def traduzir_texto(texto, de="pt", para="en"):
    """Tradução sob demanda, baixa modelos se necessário."""
    try:
        # Baixa modelo se não estiver disponível
        baixar_modelo(de, para)

        # Atualiza lista de idiomas instalados
        idiomas_instalados = argostranslate.translate.get_installed_languages()
        idioma_origem = next((i for i in idiomas_instalados if i.code == de), None)
        idioma_destino = next((i for i in idiomas_instalados if i.code == para), None)

        if idioma_origem and idioma_destino:
            traducao = idioma_origem.get_translation(idioma_destino)
            return traducao.translate(texto)
        else:
            print(f"Idiomas não encontrados: {de} -> {para}")
            return texto

    except Exception as e:
        print(f"Erro ao traduzir: {e}")
        return texto
