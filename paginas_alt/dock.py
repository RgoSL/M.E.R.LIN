# Import das Bibliotecas Utilizadas
from customtkinter import *
from PIL import Image

# Import das Classes com as Funcionalidades da Dock
from func_nao_visual.lista_apps import abrir_lista_apps
from func_nao_visual.comandos_dock import btns
from func_nao_visual.lista_apps import carregar_apps_em_thread

class Dock(CTkToplevel):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        # Lista para navegação entre botões
        self.botoes_dock = []
        self.botao_selecionado = 0

        # Posicionamento da Dock
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.wm_attributes("-transparentcolor", "#654E82") 

        # Posicionamento da Dock na Tela
        altura_tela = self.winfo_screenheight()
        largura_tela = self.winfo_screenwidth()
        largura_dock = 80
        altura_dock = 370
        offset = 55
        dock_x = largura_tela - largura_dock        # direita da tela
        dock_y = altura_tela - altura_dock - offset        # inferior da tela
        self.geometry(f"{largura_dock}x{altura_dock}+{dock_x}+{dock_y}")

        # Container Principal
        Frame = CTkFrame(self, bg_color="#654E82", fg_color = "#644C81", border_width = 1, border_color = "#f9b14f", corner_radius = 10)
        Frame.pack(fill="both", expand=True)

        # Definição do Formato dos Botões da Dock
        def btns_dock(caminho, command = None):
            Btn = Image.open(caminho)
            Btn = Btn.resize((150, 120))
            Btn = CTkImage(light_image = Btn, dark_image = Btn)
            
            # Formato de Botão dos Icones da Dock
            Bot = CTkButton(
                Frame,
                image = Btn,
                text = "",
                width = 60,
                height = 60,
                fg_color = "#432D5D",
                hover_color = "#C58ADE",
                corner_radius = 10,
                command = command
            )
            Bot.image = Btn
            Bot.pack(pady = 8)

            # Passa os Botões da Dock Para uma Lista
            self.botoes_dock.append(Bot)
            return Bot

        # Botões da Dock, Funcionalidade de Cada um Sendo Ativada por uma Lambda
        btns_dock("assets/ImgsDock/LApps.png", command=lambda: carregar_apps_em_thread(self))
        btns_dock("assets/ImgsDock/pacotes.png", command=lambda: btns.Btn_Pacotes(self.controller))
        btns_dock("assets/ImgsDock/navegador.png", command=lambda: btns.Btn_Navegador())
        btns_dock("assets/ImgsDock/teclado.png", command=lambda: btns.Btn_Teclado(self))
        btns_dock("assets/ImgsDock/Fechar.png", command=lambda: btns.Btn_Fechar(self))

        # Borda dos Botões Selecionados
        def atualizar_selecao():
            for i, botao in enumerate(self.botoes_dock):
                if i == self.botao_selecionado:
                    botao.configure(border_width=2, border_color="#f9b14f")
                else:
                    botao.configure(border_width=0)

        atualizar_selecao()

        # Chamada da Função de Seleção ao Pressionar o Tab
        def navegar(event=None):
            self.botao_selecionado = (self.botao_selecionado + 1) % len(self.botoes_dock)
            atualizar_selecao()
            return "break"  

        # Função de Ativação do Botão Selecionado com o Enter
        def ativar(event=None):
            botao = self.botoes_dock[self.botao_selecionado]
            botao.invoke()
            return "break"

        # Atribuição das Funções às Teclas
        self.bind("<Tab>", navegar)
        self.bind("<Return>", ativar)
        self.focus_set()