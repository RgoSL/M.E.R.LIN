# comandos_dock.py
from lista_apps import AppList
from eye_tracking.navegacao import EyeControl
from cv2 import destroyWindow
class btns:
    @staticmethod
    def Btn_Lista():        
        AppList()

    @staticmethod
    def Btn_Pacotes():
        print("Pacotes")

    @staticmethod
    def Btn_Navegador():
        eye =EyeControl()
        eye.start()
       

    @staticmethod
    def Btn_Fechar(dock):
        dock.destroy()
        dock.destroyWindow()

