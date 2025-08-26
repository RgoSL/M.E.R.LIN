# Essa classe guarda a ação que vai ser executada com a detecção do olhar

import subprocess
process = None

def open_app(path="notepad.exe"):
    global process
    if process is None:
        process = subprocess.Popen([path])
        print(f"Aplicativo aberto: {path}")

def close_app():
    global process
    if process is not None:
        process.terminate()
        print("Aplicativo fechado.")
        process = None
