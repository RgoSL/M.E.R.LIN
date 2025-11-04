import cv2
import mediapipe as mp
import pyautogui
import time
import keyboard
import sys
import threading
import queue

class EyeControl:
    def __init__(self, cam_index=0, width=640, height=360, frame_skip=2):
        # parâmetros de captura
        self.cam_index = cam_index
        self.width = width
        self.height = height
        self.frame_skip = max(1, frame_skip)

        # MediaPipe (será criado no worker thread)
        self.mp_face_mesh = mp.solutions.face_mesh

        # índices dos olhos (como antes)
        self.LEFT_EYE = [33, 160, 158, 133, 153, 144]
        self.RIGHT_EYE = [362, 385, 387, 263, 373, 380]
        self.LEFT_TOP, self.LEFT_BOTTOM = 159, 145
        self.RIGHT_TOP, self.RIGHT_BOTTOM = 386, 374

        # thresholds / timing
        self.EAR_THRESHOLD_CLOSED = 0.25
        self.EAR_THRESHOLD_OPEN = 0.38
        self.VERTICAL_THRESHOLD = 5
        self.CLOSE_DURATION = 0.25
        self.OPEN_DURATION = 0.25
        self.DISABLE_DURATION = 3.0
        self.ACTION_COOLDOWN = 0.5

        # estado
        self.actions_active = False
        self.running = False

        # timers / debounces
        self.last_action_time = 0
        self.both_closed_start = None
        self.left_closed_start = None
        self.right_closed_start = None
        self.eyes_open_start = None
        self.last_toggle_time = 0
        self.toggle_debounce = 0.8

        # scroll suave
        self.last_scroll_time = 0
        self.scroll_delay = 0.03

        # threads & queues
        self.frame_queue = queue.Queue(maxsize=2)
        self.result_queue = queue.Queue(maxsize=2)
        self.worker_thread = None
        self.capture_thread = None

        # captura (inicializa no start)
        self.cap = None

        # aumentar performance opencv
        cv2.setUseOptimized(True)
        self.worker_thread = None

    # -------------------------------------------------------
    # Utilitários
    # -------------------------------------------------------
    def eye_aspect_ratio(self, landmarks, eye_indices, w, h):
        coords = [(int(landmarks[i].x * w), int(landmarks[i].y * h)) for i in eye_indices]
        A = ((coords[1][1] - coords[5][1]) ** 2 + (coords[1][0] - coords[5][0]) ** 2) ** 0.5
        B = ((coords[2][1] - coords[4][1]) ** 2 + (coords[2][0] - coords[4][0]) ** 2) ** 0.5
        C = ((coords[0][1] - coords[3][1]) ** 2 + (coords[0][0] - coords[3][0]) ** 2) ** 0.5
        return (A + B) / (2.0 * C)

    def toggle_actions(self):
        self.actions_active = not self.actions_active
        print("🟢 Ações Ativas" if self.actions_active else "🟡 Standby")

    def can_act(self):
        return time.time() - self.last_action_time >= self.ACTION_COOLDOWN

    def smooth_scroll(self, amount):
        now = time.time()
        if now - self.last_scroll_time > self.scroll_delay:
            pyautogui.scroll(int(amount))
            self.last_scroll_time = now

    # -------------------------------------------------------
    # Worker: aqui roda a inferência MediaPipe (heavy)
    # pega frames da frame_queue e coloca frames processados em result_queue
    # -------------------------------------------------------
    def worker_process(self):
        print("Worker de inferência iniciado.")
        # Criar o FaceMesh aqui, dentro da thread worker
        with self.mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True) as face_mesh:
            while self.running:
                try:
                    frame = self.frame_queue.get(timeout=0.5)
                except queue.Empty:
                    continue

                # processa o frame (inferencia + anotação)
                processed = self._process_frame_inference(frame, face_mesh)
                # tenta colocar no result_queue (descarta se estiver cheio para evitar backlog)
                try:
                    self.result_queue.put_nowait(processed)
                except queue.Full:
                    pass  # se estiver cheio, este frame é descartado

        print("Worker de inferência finalizado.")

    # processamento que usa mediapipe (separa da lógica de exibição)
    def _process_frame_inference(self, frame, face_mesh):
        h, w, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_frame)
        current_time = time.time()

        # A lógica de ações depende de results e landmarks
        if results.multi_face_landmarks and self.actions_active:
            landmarks = results.multi_face_landmarks[0].landmark

            left_ear = self.eye_aspect_ratio(landmarks, self.LEFT_EYE, w, h)
            right_ear = self.eye_aspect_ratio(landmarks, self.RIGHT_EYE, w, h)
            ear_avg = (left_ear + right_ear) / 2

            left_eye_vert = (landmarks[self.LEFT_TOP].y - landmarks[self.LEFT_BOTTOM].y) * h
            right_eye_vert = (landmarks[self.RIGHT_TOP].y - landmarks[self.RIGHT_BOTTOM].y) * h
            left_closed = left_ear < self.EAR_THRESHOLD_CLOSED and left_eye_vert < self.VERTICAL_THRESHOLD
            right_closed = right_ear < self.EAR_THRESHOLD_CLOSED and right_eye_vert < self.VERTICAL_THRESHOLD

            # Scroll contínuo baseado no nariz
            nose_y = landmarks[1].y * h
            center_zone_top = h * 0.45
            center_zone_bottom = h * 0.55
            if nose_y < center_zone_top or nose_y > center_zone_bottom:
                offset = (h * 0.5 - nose_y) / (h * 0.5)
                scroll_amount = offset * 50
                scroll_amount = max(min(scroll_amount, 30), -30)
                self.smooth_scroll(scroll_amount)

            # Ambos fechados
            if left_closed and right_closed:
                if self.both_closed_start is None:
                    self.both_closed_start = current_time
                duration_closed = current_time - self.both_closed_start

                if duration_closed >= self.CLOSE_DURATION and self.can_act() and duration_closed < self.DISABLE_DURATION:
                    pyautogui.press("tab")
                    print("TAB pressionado!")
                    self.last_action_time = current_time

                elif duration_closed >= self.DISABLE_DURATION:
                    print("🔴 Ambos os olhos fechados por tempo limite — encerrando...")
                    self.stop()
                    # NÃO chame sys.exit() no worker; deixe o main lidar com encerramento
                    return frame

                self.left_closed_start = None
                self.right_closed_start = None
            else:
                self.both_closed_start = None

                if right_closed and not left_closed:
                    if self.right_closed_start is None:
                        self.right_closed_start = current_time
                    elif current_time - self.right_closed_start >= self.CLOSE_DURATION and self.can_act():
                        pyautogui.press("enter")
                        print("ENTER com olho direito!")
                        self.last_action_time = current_time
                        self.right_closed_start = None
                else:
                    self.right_closed_start = None

                if left_closed and not right_closed:
                    if self.left_closed_start is None:
                        self.left_closed_start = current_time
                    elif current_time - self.left_closed_start >= self.CLOSE_DURATION and self.can_act():
                        pyautogui.press("backspace")
                        print("BACKSPACE com olho esquerdo!")
                        self.last_action_time = current_time
                        self.left_closed_start = None
                else:
                    self.left_closed_start = None

            if ear_avg > self.EAR_THRESHOLD_OPEN:
                if self.eyes_open_start is None:
                    self.eyes_open_start = current_time
                elif current_time - self.eyes_open_start >= self.OPEN_DURATION and self.can_act():
                    pyautogui.press("f6")
                    print("F6 com olhos bem abertos!")
                    self.last_action_time = current_time
                    self.eyes_open_start = None
            else:
                self.eyes_open_start = None

            # desenha pontos dos olhos
            for idx in self.LEFT_EYE + self.RIGHT_EYE:
                x = int(landmarks[idx].x * w)
                y = int(landmarks[idx].y * h)
                cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

        return frame

    # -------------------------------------------------------
    # Loop principal (captura + exibição). Este método é bloqueante,
    # portanto chame via thread se quiser que não bloqueie a UI.
    # -------------------------------------------------------
    def start(self):
        if self.running:
            print("EyeControl já está rodando.")
            return

        self.running = True
        self.worker_thread = threading.current_thread()
        # iniciar captura
        self.cap = cv2.VideoCapture(self.cam_index, cv2.CAP_DSHOW if sys.platform.startswith("win") else 0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

        # iniciar worker de inferência
        self.worker_thread = threading.Thread(target=self.worker_process, daemon=True)
        self.worker_thread.start()

        print("Iniciando loop principal (capture/display). Pressione ESC para sair.")
        frame_count = 0

        try:
            while self.running:
                ret, frame = self.cap.read()
                if not ret:
                    time.sleep(0.01)
                    continue

                frame = cv2.flip(frame, 1)
                frame_count += 1

                # toggle via teclado (Ctrl+Alt)
                current_time = time.time()
                if keyboard.is_pressed("ctrl") and keyboard.is_pressed("alt") and current_time - self.last_toggle_time > self.toggle_debounce:
                    self.toggle_actions()
                    self.last_toggle_time = current_time

                # envia para o worker apenas alguns frames p/ aliviar processamento
                if frame_count % self.frame_skip == 0:
                    try:
                        # não bloqueia se queue estiver cheia
                        self.frame_queue.put_nowait(frame.copy())
                    except queue.Full:
                        pass

                # se worker já processou algo, pega e exibe
                try:
                    processed = self.result_queue.get_nowait()
                    display_frame = processed
                except queue.Empty:
                    display_frame = frame

                # overlay de status
                cv2.putText(display_frame, f"Ações Ativas: {self.actions_active}", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

                cv2.imshow("Olho Detector", display_frame)

                # ESC para sair
                if cv2.waitKey(1) & 0xFF == 27:
                    self.stop()
                    break

        except Exception as e:
            print("Erro no loop principal:", e)
        finally:
            self.stop()

    # -------------------------------------------------------
    # Stop / cleanup: threads serão finalizadas com running=False
    # -------------------------------------------------------
    def stop(self):
        if not self.running:
            return

        self.running = False

        # GUARANTE esperar a thread morrer
        if self.worker_thread and self.worker_thread.is_alive():
            self.worker_thread.join()

        if self.cap:
            self.cap.release()
            self.cap = None

        cv2.destroyAllWindows()
        time.sleep(0.3) # ESSENCIAL no windows



# -------------------------------------------------------
# Uso recomendado (exemplo):
# -------------------------------------------------------
# 1) Rodar em background (recomendado quando chamado pela dock):
#    eye = EyeControl()
#    threading.Thread(target=eye.start, daemon=True).start()
#
# 2) Ou rodar bloqueante (para debug direto no terminal):
#    eye = EyeControl()
#    eye.start()
#
# Para encerrar programaticamente: eye.stop()
# -------------------------------------------------------
