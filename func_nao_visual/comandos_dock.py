# comandos_dock.py
from func_nao_visual.lista_apps import AppList
from eye_tracking.navegacao import EyeControl
import threading
import sys
class btns:
    @staticmethod
    def Btn_Lista():        
        AppList()

    @staticmethod
    def Btn_Pacotes():
        print("Pacotes")

    @staticmethod
    def Btn_Navegador():
        # Cria a instância
        eye = EyeControl()
        # Executa em uma thread separada para não travar o Tkinter
        t = threading.Thread(target=eye.start, daemon=True)
        t.start()
       

    @staticmethod
    def Btn_Fechar(dock):
        dock.destroy()
        sys.exit()

