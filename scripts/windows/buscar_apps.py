# Essa Classe é Especifica Para Achar Apps no Windows

import os
import win32com.client 
import pathlib

def get_windows_apps(): # Função de Procurar Pelos Apps

    start_menu_dirs = [
        r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs", # Caminho Padrão com Programas
        os.path.join(os.environ["APPDATA"], r"Microsoft\Windows\Start Menu\Programs") # Caminho Padrão com Programas
    ]

    shell = win32com.client.Dispatch("WScript.Shell")
    apps = []

    for base_dir in start_menu_dirs:
        for root, dirs, files in os.walk(base_dir):
            for file in files:
                if file.endswith(".lnk"):
                    full_path = os.path.join(root, file)
                    try:
                        shortcut = shell.CreateShortcut(full_path)
                        target = shortcut.TargetPath
                        if os.path.isfile(target):
                            apps.append({
                                "name": pathlib.Path(file).stem,
                                "command": f'"{target}"',
                                "favorite": False
                            })
                    except Exception as e:
                        print(f"Erro ao ler {file}: {e}")

    unique_apps = {app["name"]: app for app in apps}
    apps = sorted(unique_apps.values(), key=lambda x: x["name"].lower())
    return apps