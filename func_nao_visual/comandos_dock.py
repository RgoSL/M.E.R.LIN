import subprocess
import sys
import threading

from eye_tracking.navegacao import EyeControl

from func_nao_visual.lista_apps import AppList
from func_nao_visual.teclado_open import TecladoVarreduraTab


class btns:
    @staticmethod
    def Btn_Lista():
        AppList()

    @staticmethod
    def Btn_Pacotes(controller):
        app = controller.app_selecionado
        if app:
            print("Pacotes recebeu:", app["name"])
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

    eye_instance = None

    @staticmethod
    def Btn_Navegador():
        if btns.eye_instance and btns.eye_instance.running:
            print("Já está rodando")
            return

        btns.eye_instance = EyeControl()
        t = threading.Thread(target=btns.eye_instance.start, daemon=True)
        t.start()

    @staticmethod
    def Btn_Teclado(dock_instance=None):
        tclado = TecladoVarreduraTab(dock_title=dock_instance.title())
        tclado.deiconify()

    @staticmethod
    def Btn_Fechar(dock):
        dock.destroy()
        sys.exit()
