# Classe Responsável por Centralizar as Traduções

class I18nManager:
    
    def __init__(self):
        self.idioma_atual = "pt"
        self.observers = []  # Lista de Frames Identificados
        
        # Dicionários com as Traduções
        self.traducoes = {
            "pt": {   # Dicionário em Português Brasileiro
                "titulo_principal": "Toda Magia Começa Pelas Palavras Certas",
                "idioma_software": "Idioma do Software:",
                "voltar": "Voltar",
                "avancar": "Avançar",
                "portugues": "Português",
                "ingles": "Inglês",
                "espanhol": "Espanhol",
            },
            "en": { # Dicionário em Inglês
                "titulo_principal": "All Magic Begins With The Right Words",
                "idioma_software": "Software Language:",
                "voltar": "Back",
                "avancar": "Next",
                "portugues": "Portuguese",
                "ingles": "English",
                "espanhol": "Spanish",
            },
            "es": { # Dicionário em Espanhol
                "titulo_principal": "Toda Magia Comienza Con Las Palabras Correctas",
                "idioma_software": "Idioma del Software:",
                "voltar": "Volver",
                "avancar": "Siguiente",
                "portugues": "Portugués",
                "ingles": "Inglés",
                "espanhol": "Español",
            }
        }
    
    def t(self, chave):
        # Método Para Traduzir as Chaves do Dicionário Para o Idioma Atual
        return self.traducoes.get(self.idioma_atual, {}).get(chave, chave)
    
    def mudar_idioma(self, novo_idioma):
        # Método Para Trocar os Idiomas e Atualizar a Lista Observer
        if novo_idioma in self.traducoes:
            self.idioma_atual = novo_idioma
            self.notificar_observers()
    
    def registrar_observer(self, observer):
        # Método Utilizado Para Definir um Frame Tradutível
        if observer not in self.observers:
            self.observers.append(observer)
    
    def remover_observer(self, observer):
        # Método Para Remover o Frame Definido
        if observer in self.observers:
            self.observers.remove(observer)
    
    def notificar_observers(self):
        # Método Para Informar os Frames Sobre a Troca de Idiomas
        for observer in self.observers:
            if hasattr(observer, 'atualizar_idioma'):
                observer.atualizar_idioma()

i18n = I18nManager() # Tornando a Classe Facilmente Instanciável