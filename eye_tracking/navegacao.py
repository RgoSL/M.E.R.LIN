import cv2
import mediapipe as mp
import pyautogui
import time
import sys  # 🔹 para encerramento completo opcional

class EyeControl():
    def __init__(self):
        # Inicializa MediaPipe
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True)

        # Índices dos olhos
        self.LEFT_EYE = [33, 160, 158, 133, 153, 144]
        self.RIGHT_EYE = [362, 385, 387, 263, 373, 380]

        # Pálpebras
        self.LEFT_TOP, self.LEFT_BOTTOM = 159, 145
        self.RIGHT_TOP, self.RIGHT_BOTTOM = 386, 374

        # Parâmetros
        self.EAR_THRESHOLD_CLOSED = 0.25
        self.VERTICAL_THRESHOLD = 5
        self.DISABLE_DURATION = 2  # Fecha programa se ambos olhos fechados por 3s

        # Controle
        self.cap = cv2.VideoCapture(0)
        self.both_closed_start = None
        self.actions_active = True
        self.running = True

    def eye_aspect_ratio(self, landmarks, eye_indices, w, h):
        coords = [(int(landmarks[i].x * w), int(landmarks[i].y * h)) for i in eye_indices]
        A = ((coords[1][1] - coords[5][1]) ** 2 + (coords[1][0] - coords[5][0]) ** 2) ** 0.5
        B = ((coords[2][1] - coords[4][1]) ** 2 + (coords[2][0] - coords[4][0]) ** 2) ** 0.5
        C = ((coords[0][1] - coords[3][1]) ** 2 + (coords[0][0] - coords[3][0]) ** 2) ** 0.5
        return (A + B) / (2.0 * C)

    def process_frame(self, frame):
        h, w, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)
        current_time = time.time()

        if results.multi_face_landmarks:
            landmarks = results.multi_face_landmarks[0].landmark

            # EAR
            left_ear = self.eye_aspect_ratio(landmarks, self.LEFT_EYE, w, h)
            right_ear = self.eye_aspect_ratio(landmarks, self.RIGHT_EYE, w, h)
            left_eye_vert = (landmarks[self.LEFT_TOP].y - landmarks[self.LEFT_BOTTOM].y) * h
            right_eye_vert = (landmarks[self.RIGHT_TOP].y - landmarks[self.RIGHT_BOTTOM].y) * h

            left_closed = left_ear < self.EAR_THRESHOLD_CLOSED and left_eye_vert < self.VERTICAL_THRESHOLD
            right_closed = right_ear < self.EAR_THRESHOLD_CLOSED and right_eye_vert < self.VERTICAL_THRESHOLD

            # 🔹 Fecha o programa se ambos os olhos ficarem fechados por 3 segundos
            if left_closed and right_closed:
                if self.both_closed_start is None:
                    self.both_closed_start = current_time
                elif current_time - self.both_closed_start >= self.DISABLE_DURATION:
                    print("🔴 Ambos os olhos fechados por 3s — encerrando EyeControl...")
                    self.stop()
                    # 🔹 Encerra completamente o processo (evita reabrir)
                    sys.exit(0)
            else:
                self.both_closed_start = None

            # Desenhar olhos
            for idx in self.LEFT_EYE + self.RIGHT_EYE:
                x = int(landmarks[idx].x * w)
                y = int(landmarks[idx].y * h)
                cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

        return frame

    def start(self):
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            frame = self.process_frame(frame)

            cv2.putText(frame, f"Ações Ativas: {self.actions_active}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            cv2.imshow("Olho Detector", frame)
            if cv2.waitKey(1) & 0xFF == 27:  # ESC fecha
                self.stop()
                break

    def stop(self):
        self.running = False
        try:
            if self.cap.isOpened():
                self.cap.release()
        except:
            pass
        cv2.destroyAllWindows()
        print("✅ EyeControl FINALIZADO")
