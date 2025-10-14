import cv2
import mediapipe as mp
import pyautogui
import time
import keyboard
import sys

class EyeControl:
    def __init__(self):
        # Inicializa MediaPipe
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True)

        # Índices dos olhos
        self.LEFT_EYE = [33, 160, 158, 133, 153, 144]
        self.RIGHT_EYE = [362, 385, 387, 263, 373, 380]
        self.LEFT_TOP, self.LEFT_BOTTOM = 159, 145
        self.RIGHT_TOP, self.RIGHT_BOTTOM = 386, 374

        # Parâmetros de detecção
        self.EAR_THRESHOLD_CLOSED = 0.25
        self.EAR_THRESHOLD_OPEN = 0.38
        self.VERTICAL_THRESHOLD = 5
        self.CLOSE_DURATION = 0.25
        self.OPEN_DURATION = 0.25
        self.DISABLE_DURATION = 2
        self.ACTION_COOLDOWN = 0.5

        # Controle
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 640)
        self.cap.set(4, 360)
        self.actions_active = False
        self.running = True

        # Temporizadores
        self.last_action_time = 0
        self.both_closed_start = None
        self.left_closed_start = None
        self.right_closed_start = None
        self.eyes_open_start = None
        self.last_toggle_time = 0
        self.toggle_debounce = 0.8

        # Scroll suave
        self.last_scroll_time = 0
        self.scroll_delay = 0.03  # tempo mínimo entre scrolls (30ms)

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
        """Executa um scroll suave e proporcional."""
        now = time.time()
        if now - self.last_scroll_time > self.scroll_delay:
            pyautogui.scroll(int(amount))
            self.last_scroll_time = now

    def process_frame(self, frame):
        h, w, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)
        current_time = time.time()

        # Toggle com Ctrl+Alt
        if keyboard.is_pressed("ctrl") and keyboard.is_pressed("alt") and current_time - self.last_toggle_time > self.toggle_debounce:
            self.toggle_actions()
            self.last_toggle_time = current_time

        if results.multi_face_landmarks and self.actions_active:
            landmarks = results.multi_face_landmarks[0].landmark

            left_ear = self.eye_aspect_ratio(landmarks, self.LEFT_EYE, w, h)
            right_ear = self.eye_aspect_ratio(landmarks, self.RIGHT_EYE, w, h)
            ear_avg = (left_ear + right_ear) / 2

            left_eye_vert = (landmarks[self.LEFT_TOP].y - landmarks[self.LEFT_BOTTOM].y) * h
            right_eye_vert = (landmarks[self.RIGHT_TOP].y - landmarks[self.RIGHT_BOTTOM].y) * h
            left_closed = left_ear < self.EAR_THRESHOLD_CLOSED and left_eye_vert < self.VERTICAL_THRESHOLD
            right_closed = right_ear < self.EAR_THRESHOLD_CLOSED and right_eye_vert < self.VERTICAL_THRESHOLD

            # ==============================
            # 🧭 SCROLL CONTÍNUO SUAVE
            # ==============================
            nose_y = landmarks[1].y * h
            center_zone_top = h * 0.45
            center_zone_bottom = h * 0.55

            if nose_y < center_zone_top or nose_y > center_zone_bottom:
                # distância do centro (normalizada)
                offset = (h * 0.5 - nose_y) / (h * 0.5)
                scroll_amount = offset * 50  # fator de intensidade
                scroll_amount = max(min(scroll_amount, 30), -30)  # limite de velocidade
                self.smooth_scroll(scroll_amount)
            # ==============================

            # --------------------------------------------
            # 🔹 Ações com olhos
            # --------------------------------------------
            if left_closed and right_closed:
                if self.both_closed_start is None:
                    self.both_closed_start = current_time
                elif current_time - self.both_closed_start >= self.CLOSE_DURATION and self.can_act():
                    pyautogui.press("tab")
                    print("TAB pressionado!")
                    self.last_action_time = current_time
                    self.both_closed_start = None

                self.left_closed_start = None
                self.right_closed_start = None

                if current_time - (self.both_closed_start or current_time) >= self.DISABLE_DURATION:
                    print("🔴 Ambos os olhos fechados por 3s — encerrando...")
                    self.stop()
                    sys.exit(0)

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

            # Desenha olhos
            for idx in self.LEFT_EYE + self.RIGHT_EYE:
                x = int(landmarks[idx].x * w)
                y = int(landmarks[idx].y * h)
                cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

        return frame

    def start(self):
        frame_skip = 0
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                break

            frame_skip += 1
            if frame_skip % 2 != 0:
                continue

            frame = cv2.flip(frame, 1)
            frame = self.process_frame(frame)

            cv2.putText(frame, f"Ações Ativas: {self.actions_active}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.imshow("Olho Detector", frame)

            if cv2.waitKey(1) & 0xFF == 27:
                self.stop()
                break

    def stop(self):
        self.running = False
        if self.cap.isOpened():
            self.cap.release()
        cv2.destroyAllWindows()
        print("✅ EyeControl FINALIZADO")


if __name__ == "__main__":
    eye_control = EyeControl()
    print("Clique na janela do NAVEGADOR após iniciar para receber os comandos.")
    time.sleep(2)
    eye_control.start()