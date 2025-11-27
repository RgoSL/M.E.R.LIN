import math
import time
import pyautogui as py
import pygetwindow as gw
from customtkinter import *

from func_visual.modos.sistema_cores import cores
from eye_tracking.track_central import gerenciador, eye_aspect_ratio

class TecladoVarreduraTab(CTk):
    def __init__(
        self,
        cooldown=0.2,
        ear_threshold=0.20,
        both_eyes_time=0.25,
        right_eye_time=0.50,
        close_app_time=2.0,
        surprise_open_time=0.25,
        dock_title=None,
    ):
        super().__init__()
        
        self.cores = cores()
        self.cliente_id = "teclado"
        
        self.dock_title = dock_title
        self.title("Teclado de Varredura")
        self.resizable(False, False)
        self.attributes("-topmost", True)
        
        # Configurações da Detecção
        self.cooldown = float(cooldown)
        self.ear_threshold = float(ear_threshold)
        self.both_eyes_time = float(both_eyes_time)
        self.right_eye_time = float(right_eye_time)
        self.close_app_time = float(close_app_time)
        self.surprise_open_time = float(surprise_open_time)
        
        # Estados
        self.ultimo_acao_t = 0.0
        self.eyes_open_start = None
        self.both_closed_start = None
        self.right_closed_start = None
        self.close_app_start = None
        
        self.widget_destino = None
        
        self.LEFT_EYE = [33, 160, 158, 133, 153, 144]
        self.RIGHT_EYE = [362, 385, 387, 263, 373, 380]
        
        self.layout_completo = [
            ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "Backspace"],
            ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
            ["A", "S", "D", "F", "G", "H", "J", "K", "L", "Digitar Texto"],
            ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "Espaço"],
        ]

        self.criar_interface()
        
        self.botoes = []
        self.indice_tab = 0
        self.tab_direcao = 1
        self.carregar_teclas()

        self.bind("<Tab>", self.tab_seguinte)
        self.bind("<Return>", self.confirmar_tecla)
        self.bind("<Left>", lambda e: self.mudar_direcao(-1))
        self.bind("<Right>", lambda e: self.mudar_direcao(1))
        self.bind("<FocusIn>", self._on_focus_in)
        self.bind("<FocusOut>", self._on_focus_out)
        
        self.focus_force()
        self.destacar_tecla(self.indice_tab)

        gerenciador.registrar_cliente(
            self.cliente_id,
            self._processar_deteccao,
            ativo=True
        )

        self.protocol("WM_DELETE_WINDOW", self._on_closing)

    def criar_interface(self):
        self.entrada = CTkEntry(
            self,
            width=600,
            height=35,
            font=("Arial", 14),
            text_color=self.cores["texto_principal"],
            fg_color=self.cores["fundo_secundario"],
            border_color=self.cores["borda_principal"],
        )
        self.entrada.pack(padx=10, pady=5)

        self.botao_enviar = CTkButton(
            self,
            text="Digitar Texto",
            fg_color=self.cores["botao_normal"],
            hover_color=self.cores["hover"],
            text_color=self.cores["texto_botao"],
            width=150,
            height=40,
            font=("Arial", 12),
            command=self.enviar_texto,
        )
        self.botao_enviar.pack(pady=5)

        self.frame_teclado = CTkFrame(
            self,
            fg_color=self.cores["fundo_frame"]
        )
        self.frame_teclado.pack(padx=10, pady=10)

    def carregar_teclas(self):
        for widget in self.frame_teclado.winfo_children():
            widget.destroy()
        self.botoes.clear()
        
        for r_idx, linha in enumerate(self.layout_completo):
            for c_idx, tecla in enumerate(linha):
                botao = CTkButton(
                    self.frame_teclado,
                    text=tecla,
                    text_color=self.cores["texto_botao"],
                    fg_color=self.cores["botao_normal"],
                    hover_color=self.cores["hover"],
                    width=50,
                    height=40,
                    command=lambda t=tecla: self.adicionar_a_entrada(t),
                )
                botao.grid(row=r_idx, column=c_idx, padx=2, pady=2)
                self.botoes.append(botao)

    def _processar_deteccao(self, resultado):
        landmarks = resultado.get("landmarks")
        if not landmarks:
            # Reset nos Valores se não identificar Rostos
            self.both_closed_start = None
            self.right_closed_start = None
            self.close_app_start = None
            self.eyes_open_start = None
            return

        w = resultado["width"]
        h = resultado["height"]
        now = time.time()

        # Calcula EAR
        left_ear = eye_aspect_ratio(landmarks, self.LEFT_EYE, w, h)
        right_ear = eye_aspect_ratio(landmarks, self.RIGHT_EYE, w, h)
        ear_avg = (left_ear + right_ear) / 2

        both_closed = (
            right_ear < self.ear_threshold and left_ear < self.ear_threshold
        )

        # Muito Tempo Fechado Encerra Tudo
        if both_closed:
            if self.close_app_start is None:
                self.close_app_start = now
            elif now - self.close_app_start >= self.close_app_time:
                self.after(0, self._on_closing)
                return
        else:
            self.close_app_start = None

        # Com os Olhos Fechados Ele dá Tab
        if both_closed:
            if self.both_closed_start is None:
                self.both_closed_start = now
            elif now - self.both_closed_start >= self.both_eyes_time:
                if now - self.ultimo_acao_t >= self.cooldown:
                    self.after(0, self.tab_seguinte)
                    self.ultimo_acao_t = now
                    self.both_closed_start = None
        else:
            self.both_closed_start = None

        # Com o Olho Direito Fechado Ele dá Enter
        if right_ear < self.ear_threshold and left_ear >= self.ear_threshold:
            if self.right_closed_start is None:
                self.right_closed_start = now
            elif now - self.right_closed_start >= self.right_eye_time:
                if now - self.ultimo_acao_t >= self.cooldown:
                    self.after(0, self.confirmar_tecla)
                    self.ultimo_acao_t = now
                    self.right_closed_start = None
        else:
            self.right_closed_start = None

        # Com os Olhos Muito Abertos Ele Digita
        if ear_avg > 0.38:
            if self.eyes_open_start is None:
                self.eyes_open_start = now
            elif now - self.eyes_open_start >= self.surprise_open_time:
                if now - self.ultimo_acao_t >= self.cooldown:
                    self.after(0, self.enviar_texto)
                    self.ultimo_acao_t = now
                    self.eyes_open_start = None
        else:
            self.eyes_open_start = None

    def _on_focus_in(self, event=None):
        gerenciador.ativar_cliente(self.cliente_id)
        print(f"Teclado em foco")

    def _on_focus_out(self, event=None):
        gerenciador.desativar_cliente(self.cliente_id)
        print(f"Teclado sem foco")

    def atualizar_tema(self):
        self.cores = cores()
        self.entrada.configure(
            text_color=self.cores["texto_principal"],
            fg_color=self.cores["fundo_secundario"],
            border_color=self.cores["borda_principal"]
        )
        self.botao_enviar.configure(
            fg_color=self.cores["botao_normal"],
            hover_color=self.cores["hover"],
            text_color=self.cores["texto_botao"]
        )
        self.frame_teclado.configure(fg_color=self.cores["fundo_frame"])
        for botao in self.botoes:
            botao.configure(
                text_color=self.cores["texto_botao"],
                fg_color=self.cores["botao_normal"],
                hover_color=self.cores["hover"]
            )
        self.destacar_tecla(self.indice_tab)

    def tab_seguinte(self, event=None):
        try:
            self.remover_destaque(self.indice_tab)
        except Exception:
            pass
        self.indice_tab += self.tab_direcao
        if self.indice_tab >= len(self.botoes):
            self.indice_tab = 0
        elif self.indice_tab < 0:
            self.indice_tab = len(self.botoes) - 1
        self.destacar_tecla(self.indice_tab)
        return "break"

    def mudar_direcao(self, direcao):
        self.tab_direcao = direcao

    def destacar_tecla(self, idx):
        if 0 <= idx < len(self.botoes):
            self.botoes[idx].configure(
                border_width=2,
                border_color=self.cores["borda_destaque"]
            )

    def remover_destaque(self, idx):
        if 0 <= idx < len(self.botoes):
            self.botoes[idx].configure(border_width=0)

    def confirmar_tecla(self, event=None):
        tecla = self.botoes[self.indice_tab].cget("text")
        self.adicionar_a_entrada(tecla)

    def adicionar_a_entrada(self, tecla):
        if tecla == "Backspace":
            texto = self.entrada.get()
            if texto:
                self.entrada.delete(len(texto) - 1, END)
        elif tecla == "Espaço":
            self.entrada.insert(END, " ")
        elif tecla == "Digitar Texto":
            self.enviar_texto()
        else:
            self.entrada.insert(END, tecla)

    def enviar_texto(self):
        texto_para_digitar = self.entrada.get()
        if not texto_para_digitar:
            return

        if self.widget_destino is not None:
            try:
                if hasattr(self.widget_destino, "winfo_exists") and self.widget_destino.winfo_exists():
                    self.widget_destino.insert(END, texto_para_digitar)
                    self.entrada.delete(0, END)
                    return
            except Exception:
                self.widget_destino = None

        try:
            janelas = gw.getAllWindows()
            for win in janelas:
                if win.title and win.title not in [self.title(), self.dock_title]:
                    win.activate()
                    time.sleep(0.2)
                    break
        except Exception as e:
            print(f"Erro ao focar janela: {e}")

        self.withdraw()
        time.sleep(0.5)
        py.write(texto_para_digitar, interval=0.05)
        self.deiconify()
        self.entrada.delete(0, END)
        self.focus_force()

    def _on_closing(self):
        """Limpa recursos"""
        gerenciador.remover_cliente(self.cliente_id)
        self.after(100, self.destroy)