# comandos_dock.py
from func_nao_visual.lista_apps import AppList
from eye_tracking.navegacao import EyeControl
import threading
import sys
import subprocess  # necessário para abrir apps

class btns:
    @staticmethod
    def Btn_Lista():        
        AppList()

    @staticmethod
    def Btn_Pacotes(controller):
        app = controller.app_selecionado
        if app:
            print("Pacotes recebeu:", app["name"])
            # Abrir o app
            try:
                command = app.get("command")
                if command:
                    if isinstance(command, list):
                        subprocess.Popen(command, shell=False)
                    else:
                        subprocess.Popen(command, shell=True)
                else:
                    print("App não tem comando definido")
            except Exception as e:
                print(f"Erro ao abrir {app['name']}: {e}")
        else:
            print("Nenhum app selecionado")

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
