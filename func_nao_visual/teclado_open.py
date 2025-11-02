import sys
import time
import threading
import math
import queue
import cv2
import mediapipe as mp
import pyautogui as py
from customtkinter import *
import pygetwindow as gw  # para focar a janela correta

class TecladoVarreduraTab(CTk):
    def __init__(self, cooldown=0.2, ear_threshold=0.20,
                 both_eyes_time=0.25, right_eye_time=0.50, close_app_time=2.0,
                 surprise_open_time=0.25, cam_index=0,dock_title=None):
        super().__init__()
        self.dock_title = dock_title
        self.title("Teclado de Varredura")
        self.resizable(False, False)
        self.attributes('-topmost', True)
        set_default_color_theme("dark-blue")
        # Configurações de detecção
        self.cooldown = float(cooldown)
        self.ear_threshold = float(ear_threshold)
        self.both_eyes_time = float(both_eyes_time)
        self.right_eye_time = float(right_eye_time)
        self.close_app_time = float(close_app_time)
        self.surprise_open_time = float(surprise_open_time)
        self.cam_index = cam_index

        # Estado
        self.ultimo_acao_t = 0.0
        self._detector_running = True
        self.eyes_open_start = None

        # Fila para comunicação thread-safe
        self._action_queue = queue.Queue()

        # Layout do teclado
        self.layout_completo = [
            ['1','2','3','4','5','6','7','8','9','0','Backspace'],
            ['Q','W','E','R','T','Y','U','I','O','P'],
            ['A','S','D','F','G','H','J','K','L','Digitar Texto'],
            ['Z','X','C','V','B','N','M',',','.','Espaço'],
        ]

        self.entrada = CTkEntry(self, width=600, height=35, font=('Arial', 14))
        self.entrada.pack(padx=10, pady=5)

        botao_enviar = CTkButton(self, text="Digitar Texto", width=150, height=40, font=('Arial', 12),
                                 command=self.enviar_texto)
        botao_enviar.pack(pady=5)

        self.frame_teclado = CTkFrame(self, fg_color="transparent")
        self.frame_teclado.pack(padx=10, pady=10)

        self.botoes = []
        self.indice_tab = 0
        self.tab_direcao = 1
        self.carregar_teclas()

        # Bind do Tab e setas
        self.bind("<Tab>", self.tab_seguinte)
        self.bind("<Return>", self.confirmar_tecla)
        self.bind("<Left>", lambda e: self.mudar_direcao(-1))
        self.bind("<Right>", lambda e: self.mudar_direcao(1))
        self.focus_force()
        self.destacar_tecla(self.indice_tab)

        # Start detector thread (MediaPipe + OpenCV)
        t = threading.Thread(target=self._detector_loop, daemon=True)
        t.start()

        # Start polling da fila
        self.after(50, self._process_queue)

        # Handler para fechar corretamente
        self.protocol("WM_DELETE_WINDOW", self._on_closing)

    # --------------------------
    # Funções de GUI
    # --------------------------
    def carregar_teclas(self):
        for widget in self.frame_teclado.winfo_children():
            widget.destroy()
        self.botoes.clear()
        for r_idx, linha in enumerate(self.layout_completo):
            for c_idx, tecla in enumerate(linha):
                botao = CTkButton(self.frame_teclado, text=tecla, width=50, height=40,
                                  command=lambda t=tecla: self.adicionar_a_entrada(t))
                botao.grid(row=r_idx, column=c_idx, padx=2, pady=2)
                self.botoes.append(botao)

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
            botao = self.botoes[idx]
            botao.configure(border_width=3, border_color="red")

    def remover_destaque(self, idx):
        if 0 <= idx < len(self.botoes):
            botao = self.botoes[idx]
            botao.configure(border_width=0)

    def confirmar_tecla(self, event=None):
        tecla = self.botoes[self.indice_tab].cget("text")
        self.adicionar_a_entrada(tecla)

    def adicionar_a_entrada(self, tecla):
        if tecla == 'Backspace':
            texto = self.entrada.get()
            if texto:
                self.entrada.delete(len(texto)-1, END)
        elif tecla == 'Espaço':
            self.entrada.insert(END, ' ')
        elif tecla == 'Digitar Texto':
            self.enviar_texto()
        else:
            self.entrada.insert(END, tecla)

    # --------------------------
    # Modificação: enviar texto para janela ativa
    # --------------------------
    def enviar_texto(self):
        texto_para_digitar = self.entrada.get()
        if not texto_para_digitar:
            return

        # Tenta focar na janela ativa que não seja o teclado
        try:
            janelas = gw.getAllWindows()
            for win in janelas:
                if win.title and win.title not in [self.title(), self.dock_title]:  # ignora o teclado
                    win.activate()
                    time.sleep(0.2)
                    break
        except Exception as e:
            print("Não foi possível focar no app:", e)

        # Agora envia o texto
        self.withdraw()
        time.sleep(0.5)
        py.write(texto_para_digitar, interval=0.05)
        self.deiconify()
        self.entrada.delete(0, END)
        self.focus_force()

    # --------------------------
    # Detector (thread segura)
    # --------------------------
    def _detector_loop(self):
        mp_face_mesh = mp.solutions.face_mesh
        face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True,
                                          min_detection_confidence=0.5, min_tracking_confidence=0.5)
        cap = cv2.VideoCapture(self.cam_index, cv2.CAP_DSHOW)
        if not cap.isOpened():
            print(f"Erro: não foi possível abrir a câmera index {self.cam_index}")
            return

        RIGHT_EYE = [33, 160, 158, 133, 153, 144]
        LEFT_EYE  = [362, 385, 387, 263, 373, 380]

        right_closed_since = None
        both_closed_since = None
        close_app_since = None

        try:
            while self._detector_running and cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    time.sleep(0.01)
                    continue

                small = cv2.resize(frame, (0,0), fx=0.6, fy=0.6)
                img_rgb = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)
                results = face_mesh.process(img_rgb)
                h, w = small.shape[:2]
                left_ear, right_ear = 1.0, 1.0

                if results.multi_face_landmarks:
                    lm = results.multi_face_landmarks[0].landmark

                    def landmark_point(idx):
                        p = lm[idx]
                        return int(p.x * w), int(p.y * h)

                    try:
                        r_points = [landmark_point(i) for i in RIGHT_EYE]
                        l_points = [landmark_point(i) for i in LEFT_EYE]
                    except Exception:
                        time.sleep(0.001)
                        continue

                    def euclid(a,b):
                        return math.hypot(a[0]-b[0], a[1]-b[1])

                    def ear(p1,p2,p3,p4,p5,p6):
                        vertical = euclid(p2,p6)+euclid(p3,p5)
                        horizontal = euclid(p1,p4)
                        return vertical/(2*horizontal) if horizontal != 0 else 1.0

                    right_ear = ear(*r_points)
                    left_ear = ear(*l_points)
                    ear_avg = (right_ear + left_ear)/2

                now = time.time()
                both_closed = right_ear < self.ear_threshold and left_ear < self.ear_threshold

                # Fechamento prolongado → Close app
                if both_closed:
                    if close_app_since is None:
                        close_app_since = now
                    elif now - close_app_since >= self.close_app_time:
                        self._action_queue.put("CLOSE")
                        self.ultimo_acao_t = now
                        close_app_since = both_closed_since = right_closed_since = None
                        time.sleep(0.01)
                        continue
                else:
                    close_app_since = None

                # Both eyes TAB
                if both_closed:
                    if both_closed_since is None:
                        both_closed_since = now
                    elif now - both_closed_since >= self.both_eyes_time:
                        if now - self.ultimo_acao_t >= self.cooldown:
                            self._action_queue.put("TAB")
                            self.ultimo_acao_t = now
                            both_closed_since = right_closed_since = None
                else:
                    both_closed_since = None

                # Right-eye ENTER
                if right_ear < self.ear_threshold and left_ear >= self.ear_threshold:
                    if right_closed_since is None:
                        right_closed_since = now
                    elif now - right_closed_since >= self.right_eye_time:
                        if now - self.ultimo_acao_t >= self.cooldown:
                            self._action_queue.put("ENTER")
                            self.ultimo_acao_t = now
                            right_closed_since = both_closed_since = None
                else:
                    right_closed_since = None

                # Surpresa (olhos bem abertos) → Digitar Texto
                if ear_avg > 0.38:
                    if self.eyes_open_start is None:
                        self.eyes_open_start = now
                    elif now - self.eyes_open_start >= self.surprise_open_time:
                        if now - self.ultimo_acao_t >= self.cooldown:
                            self._action_queue.put("DIGITAR")
                            self.ultimo_acao_t = now
                            self.eyes_open_start = None
                else:
                    self.eyes_open_start = None

                time.sleep(0.01)
        finally:
            cap.release()
            face_mesh.close()

    # --------------------------
    # Polling da fila
    # --------------------------
    def _process_queue(self):
        while not self._action_queue.empty():
            action = self._action_queue.get()
            if action == "TAB":
                self.tab_seguinte()
            elif action == "ENTER":
                self.confirmar_tecla()
            elif action == "DIGITAR":
                self.enviar_texto()
            elif action == "CLOSE":
                self._on_closing()
        self.after(50, self._process_queue)

    # --------------------------
    # Fechar app de forma segura
    # --------------------------
    def _on_closing(self):
        self._detector_running = False
        self.after(100, self.destroy)


if __name__ == "__main__":
    app = TecladoVarreduraTab()
    app.mainloop()
