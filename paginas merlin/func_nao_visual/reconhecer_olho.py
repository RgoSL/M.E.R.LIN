# Essa classe faz o reconhecimento facial, detecta através de um modelo do dlib os pontos de interesse do rosto

import cv2
import dlib # Dlib é uma biblioteca que age junto do cv2 para reconhecimento facial. É um modelo pronto famoso.

face_detector = dlib.get_frontal_face_detector()
landmark_predictor = dlib.shape_predictor("models/shape_predictor_68_face_landmarks.dat") # Definindo o caminho onde o modelo está salvo

def detect_blink(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_detector(gray)

    for face in faces:
        landmarks = landmark_predictor(gray, face)
        left_eye = landmarks.part(36).y - landmarks.part(37).y # Definindo interesse em pontos especificos dos 68 que a dlib reconhece
        right_eye = landmarks.part(42).y - landmarks.part(43).y 

        if left_eye < 2 and right_eye < 2: 
            return "blink"
    return None
