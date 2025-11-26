# Classe Responsável por Centralizar as Traduções

class I18nManager:
    
    def __init__(self):
        self.idioma_atual = "pt"
        self.observers = []  # Lista de Frames Identificados
        
        # Dicionários com as Traduções
        self.traducoes = {
            "pt": {   # Dicionário em Português Brasileiro
                
                # Chaves Para Trocar os Títulos de Cada Tela
                "titulo_idiomas": "Toda Magia Começa Pelas Palavras Certas",
                "idioma_software": "Idioma do Software:",
                "titulo_impressao": "Bem-Vindo(a) ao M.E.R.LIN" ,
                "titulo_temas": "Estilo é Poder. Qual o Seu?",
                "titulo_sos": "Escolha a Base dos Seus Feitiços",
                "titulo_config": "Escolha Como se Preparar",
                "titulo_termos": "Nossas Regras",
                "titulo_inicial": "Seus Feitiços",
                "titulo_ajustes": "Ajustes",
                
                # Chaves Para Trocar os Subtítulos de Cada Tela
                "subtitulo_impressao": "Configurando o Poder",
                "subtitulo_config": "Tipo de Configuração",
                
                # Chaves Para Trocar as Opções da Tela de Modo de Configuração
                "config_rpd": "Rápida",
                "config_per": "Personalizada",
                
                # Chaves Para Trocar as Opções do AlertCTK na Tela de Modo de Configuração
                "alerta": "Atenção!",
                "mensagem_alerta": "Por favor, escolha uma das opções",
                
                # Chaves Para Trocar os Textos Presentes na Tela de Ajustes
                "ajuste_camera": "Câmera",
                "ajuste_lingua": "Língua",
                "ajuste_termos": "Termos de Uso",
                
                # Chave do Texto na Tela de Termos de Uso
                "texto_termos": "Ao utilizar o M.E.R.LIN, você concorda com os seguintes termos e condições. "
                    "Nosso serviço é projetado para melhorar a acessibilidade e a interação por meio de recursos "
                    "de webcam, respeitando a sua privacidade e segurança. É importante que você tenha ciência de "
                    "que coletamos dados de vídeo apenas para a finalidade de fornecer a funcionalidade do serviço, "
                    "com total transparência e conformidade com as regulamentações de privacidade.",
                    
                # Chave Para Trocar o Nome de Cada Tema 
                "tema_claro": "Tema Claro",
                "tema_escuro": "Tema Escuro" ,
                
                # Chaves Para Trocar o Nome Dos Pacotes
                "pacote1": "Pacote 1",
                "pacote2": "Pacote 2",
                "pacote3": "Pacote 3",
                "pacote4": "Pacote 4",
                "pacote5": "Pacote 5",
                
                # Chaves Para Trocar os Botões
                "voltar": "Voltar",
                "avancar": "Avançar",
                "iniciar":"Iniciar" ,
                "finalizar": "Finalizar",
                
                # Chaves Para Trocar o Nome Dos Idiomas
                "portugues": "Português",
                "ingles": "Inglês",
                "espanhol": "Espanhol",
            },
            "en": { # Dicionário em Inglês
                
                # Chaves Para Trocar os Títulos de Cada Tela
                "titulo_idiomas": "All Magic Begins With The Right Words",
                "idioma_software": "Software Language:",
                "titulo_impressao": "Welcome to M.E.R.LIN" ,
                "titulo_temas": "Style is Power. What´s Yours?",
                "titulo_sos": "Choose the Base for Your Spells",
                "titulo_config": "Choose How to Prepare",
                "titulo_termos": "Our Rules",
                "titulo_inicial": "Your Spells",
                "titulo_ajustes": "Adjustments",
                
                # Chaves Para Trocar os Subtítulos de Cada Tela
                "subtitulo_impressao": "Setting Up Power",
                "subtitulo_config": "Configuration Type",
                
                # Chaves Para Trocar as Opções da Tela de Modo de Configuração
                "config_rpd": "Fast",
                "config_per": "Customized",
                
                # Chaves Para Trocar as Opções do AlertCTK na Tela de Modo de Configuração
                "alerta": "Warning!",
                "mensagem_alerta": "Please, choose one option",
                
                # Chaves Para Trocar os Textos Presentes na Tela de Ajustes
                "ajuste_camera": "Camera",
                "ajuste_lingua": "Language",
                "ajuste_termos": "Use Terms",
                
                # Chave do Texto na Tela de Termos de Uso
                "texto_termos": "By using M.E.R.LIN, you agree to the following terms and conditions. "
                    "Our service is designed to improve accessibility and interaction through webcam features, "
                    "respecting your privacy and security. It is important that you are aware that we collect video data "
                    "only for the purpose of providing the functionality of the service, with complete transparency "
                    "and compliance with privacy regulations.",
                    
                # Chave Para Trocar o Nome de Cada Tema 
                "tema_claro": "Light Mode",
                "tema_escuro": "Dark Mode" ,
                
                # Chaves Para Trocar o Nome Dos Pacotes
                "pacote1": "Package 1",
                "pacote2": "Package 2",
                "pacote3": "Package 3",
                "pacote4": "Package 4",
                "pacote5": "Package 5",
                
                # Chaves Para Trocar os Botões
                "voltar": "Back",
                "avancar": "Next",
                "iniciar":"Init" ,
                "finalizar": "Finish",
                
                # Chaves Para Trocar o Nome Dos Idiomas
                "portugues": "Portuguese",
                "ingles": "English",
                "espanhol": "Spanish",
            },
            "es": { # Dicionário em Espanhol
                
                # Chaves Para Trocar os Títulos de Cada Tela
                "titulo_idiomas": "Toda Magia Comienza Con Las Palabras Correctas",
                "idioma_software": "Idioma del Software:",
                "titulo_impressao": "Bienvenido a M.E.R.LIN",
                "titulo_temas": "El Estilo es Poder. ¿Cuál es el Tuyo?",
                "titulo_sos": "Elige la Base Para tus Hechizos",
                "titulo_config": "Elija Cómo Prepararse",
                "titulo_termos": "Nuestras Reglas",
                "titulo_inicial": "Tus Hechizos",
                "titulo_ajustes": "Ajustes",
                
                # Chaves Para Trocar os Subtítulos de Cada Tela
                "subtitulo_impressao": "Configurando el Poder",
                "subtitulo_config": "Tipo de Configuración",
                
                # Chaves Para Trocar as Opções da Tela de Modo de Configuração
                "config_rpd": "Rápida",
                "config_per": "Personalizada",
                
                # Chaves Para Trocar as Opções do AlertCTK na Tela de Modo de Configuração
                "alerta": "¡Atención!",
                "mensagem_alerta": "Por favor, elija una de las opciones",
                
                # Chaves Para Trocar os Textos Presentes na Tela de Ajustes
                "ajuste_camera": "Cámara",
                "ajuste_lingua": "Idioma",
                "ajuste_termos": "Términos de Uso",
                
                # Chave do Texto na Tela de Termos de Uso
                "texto_termos": "Al utilizar M.E.R.LIN, usted acepta los siguientes términos y condiciones. "
                    "Nuestro servicio está diseñado para mejorar la accesibilidad y la interacción a través de "
                    "características de cámara web, respetando su privacidad y seguridad. Es importante que sepa "
                    "que recopilamos datos de video únicamente con el propósito de proporcionar la funcionalidad "
                    "del servicio, con total transparencia y cumplimiento de las regulaciones de privacidad.",
                    
                # Chave Para Trocar o Nome de Cada Tema     
                "tema_claro": "Tema Claro",
                "tema_escuro": "Tema Oscuro",
                
                # Chaves Para Trocar o Nome Dos Pacotes
                "pacote1": "Paquete 1",
                "pacote2": "Paquete 2",
                "pacote3": "Paquete 3",
                "pacote4": "Paquete 4",
                "pacote5": "Paquete 5",
                
                # Chaves Para Trocar os Botões
                "voltar": "Volver",
                "avancar": "Siguiente",
                "iniciar": "Comenzar",
                "finalizar": "Finalizar",
                
                # Chaves Para Trocar o Nome Dos Idiomas
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