# Classe Responsável por Centralizar as Traduções

class I18nManager:
    
    def __init__(self):
        self.idioma_atual = "pt"
        self.observers = []  # Lista de Frames Identificados
        
        # Dicionários com as Traduções
        self.traducoes = {
            "pt": {   # Dicionário em Português Brasileiro
                "titulo_idiomas": "Toda Magia Começa Pelas Palavras Certas",
                "idioma_software": "Idioma do Software:",
                "titulo_impressao": "Bem-Vindo(a) ao M.E.R.LIN" ,
                "titulo_temas": "Estilo é Poder. Qual o Seu?",
                "titulo_sos": "Escolha a Base dos Seus Feitiços",
                "titulo_config": "Escolha Como se Preparar",
                "titulo_termos": "Nossas Regras",
                "titulo_inicial": "Seus Feitiços",
                "titulo_ajustes": "Ajustes",
                "subtitulo_impressao": "Configurando o Poder",
                "subtitulo_config": "Tipo de Configuração",
                "config_rpd": "Rápida",
                "config_per": "Personalizada",
                "alerta": "Atenção!",
                "mensagem_alerta": "Por favor, escolha uma das opções",
                "ajuste_camera": "Câmera",
                "ajuste_lingua": "Língua",
                "ajuste_termos": "Termos de Uso",
                "texto_termos": "Ao utilizar o M.E.R.LIN, você concorda com os seguintes termos e condições. "
                    "Nosso serviço é projetado para melhorar a acessibilidade e a interação por meio de recursos "
                    "de webcam, respeitando a sua privacidade e segurança. É importante que você tenha ciência de "
                    "que coletamos dados de vídeo apenas para a finalidade de fornecer a funcionalidade do serviço, "
                    "com total transparência e conformidade com as regulamentações de privacidade.",
                "tema_claro": "Tema Claro",
                "tema_escuro": "Tema Escuro" ,
                "pacote1": "Pacote 1",
                "pacote2": "Pacote 2",
                "pacote3": "Pacote 3",
                "pacote4": "Pacote 4",
                "pacote5": "Pacote 5",
                "voltar": "Voltar",
                "avancar": "Avançar",
                "iniciar":"Iniciar" ,
                "finalizar": "Finalizar",
                "portugues": "Português",
                "ingles": "Inglês",
                "espanhol": "Espanhol",
            },
            "en": { # Dicionário em Inglês
                "titulo_idiomas": "All Magic Begins With The Right Words",
                "idioma_software": "Software Language:",
                "titulo_impressao": "Welcome to M.E.R.LIN" ,
                "titulo_temas": "Style is Power. What´s Yours?",
                "titulo_sos": "Choose the Base for Your Spells",
                "titulo_config": "Choose How to Prepare",
                "titulo_termos": "Our Rules",
                "titulo_inicial": "Your Spells",
                "titulo_ajustes": "Adjustments",
                "subtitulo_impressao": "Setting Up Power",
                "subtitulo_config": "Configuration Type",
                "config_rpd": "Fast",
                "config_per": "Customized",
                "alerta": "Warning!",
                "mensagem_alerta": "Please, choose one option",
                "ajuste_camera": "Camera",
                "ajuste_lingua": "Language",
                "ajuste_termos": "Use Terms",
                "texto_termos": "By using M.E.R.LIN, you agree to the following terms and conditions. "
                    "Our service is designed to improve accessibility and interaction through webcam features, "
                    "respecting your privacy and security. It is important that you are aware that we collect video data "
                    "only for the purpose of providing the functionality of the service, with complete transparency "
                    "and compliance with privacy regulations.",
                "tema_claro": "Light Mode",
                "tema_escuro": "Dark Mode" ,
                "pacote1": "Package 1",
                "pacote2": "Package 2",
                "pacote3": "Package 3",
                "pacote4": "Package 4",
                "pacote5": "Package 5",
                "voltar": "Back",
                "avancar": "Next",
                "iniciar":"Init" ,
                "finalizar": "Finish",
                "portugues": "Portuguese",
                "ingles": "English",
                "espanhol": "Spanish",
            },
            "es": { # Dicionário em Espanhol
                "titulo_idiomas": "Toda Magia Comienza Con Las Palabras Correctas",
                "idioma_software": "Idioma del Software:",
                "titulo_impressao": "Bienvenido a M.E.R.LIN",
                "titulo_temas": "El Estilo es Poder. ¿Cuál es el Tuyo?",
                "titulo_sos": "Elige la Base Para tus Hechizos",
                "titulo_config": "Elija Cómo Prepararse",
                "titulo_termos": "Nuestras Reglas",
                "titulo_inicial": "Tus Hechizos",
                "titulo_ajustes": "Ajustes",
                "subtitulo_impressao": "Configurando el Poder",
                "subtitulo_config": "Tipo de Configuración",
                "config_rpd": "Rápida",
                "config_per": "Personalizada",
                "alerta": "¡Atención!",
                "mensagem_alerta": "Por favor, elija una de las opciones",
                "ajuste_camera": "Cámara",
                "ajuste_lingua": "Idioma",
                "ajuste_termos": "Términos de Uso",
                "texto_termos": "Al utilizar M.E.R.LIN, usted acepta los siguientes términos y condiciones. "
                    "Nuestro servicio está diseñado para mejorar la accesibilidad y la interacción a través de "
                    "características de cámara web, respetando su privacidad y seguridad. Es importante que sepa "
                    "que recopilamos datos de video únicamente con el propósito de proporcionar la funcionalidad "
                    "del servicio, con total transparencia y cumplimiento de las regulaciones de privacidad.",
                "tema_claro": "Tema Claro",
                "tema_escuro": "Tema Oscuro",
                "pacote1": "Paquete 1",
                "pacote2": "Paquete 2",
                "pacote3": "Paquete 3",
                "pacote4": "Paquete 4",
                "pacote5": "Paquete 5",
                "voltar": "Volver",
                "avancar": "Siguiente",
                "iniciar": "Comenzar",
                "finalizar": "Finalizar",
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