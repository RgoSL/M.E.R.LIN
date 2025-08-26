# Essa é a classe que reune as outras duas em uma só, puxando cada parte de interesse somente para ela.

import cv2
from func_nao_visual.reconhecer_olho import detect_blink
from func_nao_visual.controls import open_app, close_app

# Tem muitas opções que serviram só como debug para saber se estava tudo funcionando, por conta de alguns delays do meu PC para identificar minha webcam.

def main_loop():
    print("Iniciando loop principal...")  # Debug inicial

    cap = cv2.VideoCapture(1)
    if not cap.isOpened():
        print("Erro: não foi possível abrir a webcam!")
        return

    print("Webcam aberta com sucesso.")
    recognition_active = False
    app_opened = False

    # Nesse exemplo o reconhecimento não é automatico, ele é baseado em uma ativação por tecla
    print("Pressione 'r' para ativar/desativar reconhecimento. 'q' para sair.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Não foi possível capturar o frame.")
            break

        cv2.imshow("M.E.R.LIN - Demo", frame)

        key = cv2.waitKey(1) & 0xFF
        if key != 255: 
            print(f"Tecla pressionada: {key}")

        if key == ord("r"):
            recognition_active = not recognition_active
            print("Reconhecimento:", "Ativado" if recognition_active else "Desativado")

        if key == ord("q"):
            print("Saindo do loop...")
            break

        if recognition_active:
            event = detect_blink(frame)
            if event == "blink":
                if not app_opened:
                    open_app()
                    app_opened = True
                else:
                    close_app()
                    app_opened = False

    cap.release()
    cv2.destroyAllWindows()
    print("Loop encerrado. Webcam fechada.")

if __name__ == "__main__":
    main_loop()
