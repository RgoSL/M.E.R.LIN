# Import das Bibliotecas Utilizadas
from customtkinter import *
from PIL import Image
import threading
import os
os.environ["GLOG_minloglevel"] = "3"
os.environ["ABSL_LOGGING"] = "0"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
import cv2
import mediapipe as mp
import time

# Import das Classes com as Funcionalidades da Dock
from func_nao_visual.lista_apps import abrir_lista_apps
from func_nao_visual.comandos_dock import btns
from func_nao_visual.lista_apps import carregar_apps_em_thread

class Dock(CTkToplevel):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        # Propriedades de Atraso Para Evitar Muitas Ativações
        self.cooldown_tab = 0.6
        self.cooldown_enter = 0.6
        self.ultimo_tab = 0
        self.ultimo_enter = 0

        # Lista que Armazena os Botões da Dock a Serem Percorridos
        self.botoes_dock = []
        self.botao_selecionado = 0

        # Posicionamento da Dock
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.wm_attributes("-transparentcolor", "#654E82") 

        altura_tela = self.winfo_screenheight()
        largura_tela = self.winfo_screenwidth()
        largura_dock = 80
        altura_dock = 370
        offset = 55
        dock_x = largura_tela - largura_dock
        dock_y = altura_tela - altura_dock - offset
        self.geometry(f"{largura_dock}x{altura_dock}+{dock_x}+{dock_y}")

        # Container Principal
        Frame = CTkFrame(self, bg_color="#654E82", fg_color="#644C81",
                         border_width=1, border_color="#f9b14f", corner_radius=10)
        Frame.pack(fill="both", expand=True)

        # Definição do Formato dos Botões da Dock
        def btns_dock(caminho, command=None):
            Btn = Image.open(caminho)
            Btn = Btn.resize((150, 120))
            Btn = CTkImage(light_image=Btn, dark_image=Btn)

            Bot = CTkButton(Frame, image=Btn, text="", width=60, height=60,
                            fg_color="#432D5D", hover_color="#C58ADE",
                            corner_radius=10, command=command)
            Bot.image = Btn
            Bot.pack(pady=8)

            self.botoes_dock.append(Bot)
            return Bot

        # Botões da Dock
        btns_dock("assets/ImgsDock/LApps.png", command=lambda: carregar_apps_em_thread(self))
        btns_dock("assets/ImgsDock/pacotes.png", command=lambda: btns.Btn_Pacotes(self.controller))
        btns_dock("assets/ImgsDock/navegador.png", command=lambda: btns.Btn_Navegador())
        btns_dock("assets/ImgsDock/teclado.png", command=lambda: btns.Btn_Teclado(self))
        btns_dock("assets/ImgsDock/Fechar.png", command=lambda: btns.Btn_Fechar(self))

        # Função Para Aplicar Borda no Botão Selecionado
        def atualizar_selecao():
            for i, botao in enumerate(self.botoes_dock):
                if i == self.botao_selecionado:
                    botao.configure(border_width=2, border_color="#f9b14f")
                else:
                    botao.configure(border_width=0)

        atualizar_selecao()

        # Função de Seleção dos Botões
        def navegar(event=None):
            self.botao_selecionado = (self.botao_selecionado + 1) % len(self.botoes_dock)
            atualizar_selecao()
            return "break"
        
        # Função Para Ativar o Botão Selecionado
        def ativar(event=None):
            botao = self.botoes_dock[self.botao_selecionado]
            botao.invoke()
            return "break"

        # Atribuição das Funções às Teclas
        self.bind("<Tab>", navegar)
        self.bind("<Return>", ativar)
        self.focus_set()

        # Instância das Funções do Teclado Para uma Nova Função Baseada no Rastreio Ocular
        self.func_navegar = navegar     
        self.func_ativar = ativar

        # Instância das Threads Para uma Função
        self.executando_visao = True
        threading.Thread(target=self._controle_olhos, daemon=True).start()

    # Função Principal do Reconhecimento
    def _controle_olhos(self):
    
        mp_face = mp.solutions.face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=False, 
            static_image_mode=False,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

        cam = cv2.VideoCapture(0)
        if not cam.isOpened():
         
            return

        # Iniciando os Valores Condicionais
        tempo_blink = 0
        tempo_direita = 0

        # Loop de Ativação do Reconhecimento
        while self.executando_visao:

            # Propriedades da Captura da Imagem
            ok, frame = cam.read()
            if not ok:
                print("[ERRO] Falha ao ler frame da câmera.")
                continue

            h, w, _ = frame.shape
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            result = mp_face.process(rgb)

            if result.multi_face_landmarks:
                face = result.multi_face_landmarks[0].landmark

                # Cálculo Para a Detecção de Piscadas
                olho_sup = face[159].y * h
                olho_inf = face[145].y * h
                dist = abs(olho_sup - olho_inf)

                agora = time.time() # Essa Váriavel Aumenta a Certeza de Qual foi o Último Botão Percorrido

                # Condicional da Ativação do Enter
                if dist < 3:
                    tempo_blink += 1
                   
                else:
                                                    # Self com a Informação da Ultima Ação Ativada
                    if tempo_blink > 2 and (agora - self.ultimo_enter) > self.cooldown_enter:
                        print("[EVENTO] Enter gerado por piscada.")
                        self.ultimo_enter = agora
                        self.event_generate("<Return>")
                    tempo_blink = 0

                # Cálculo Para a Deteção da Direção do Olhar, no Caso Buscando Saber se Está Para a Direita
                nariz_x = face[1].x

                if nariz_x > 0.58:
                    tempo_direita += 1
                
                else:
                    if tempo_direita > 8 and (agora - self.ultimo_tab) > self.cooldown_tab:
                        
                        self.ultimo_tab = agora
                        self.event_generate("<Tab>")
                    tempo_direita = 0

            time.sleep(0.04)

        cam.release()