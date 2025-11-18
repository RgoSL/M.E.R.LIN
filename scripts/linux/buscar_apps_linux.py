# Essa Classe é Especifica Para Achar Apps no Linux

import configparser
import glob
import os


def get_linux_apps():  # Função que Procura Pelos Apps
    desktop_dirs = (
        [  # Definição dos Caminhos que Armazenam os Apps por Padrão em Sistemas Linux
            "/usr/share/applications",
            os.path.expanduser("~/.local/share/applications"),
            "/var/lib/flatpak/exports/share/applications",
            os.path.expanduser("~/.local/share/flatpak/exports/share/applications"),
        ]
    )

    apps = []
    seen = set()

    for directory in desktop_dirs:
        if not os.path.isdir(directory):
            continue

    for file_path in glob.glob(os.path.join(directory, "*.desktop")):
        config = configparser.ConfigParser(interpolation=None)
        try:
            config.read(file_path, encoding="utf-8")
            if "Desktop Entry" in config:
                entry = config["Desktop Entry"]
                name = entry.get("Name")
                exec_cmd = entry.get("Exec")

                if name and exec_cmd and name not in seen:
                    seen.add(name)
                    exec_cmd = exec_cmd.split()[0]
                    apps.append({"name": name, "command": exec_cmd, "favorite": False})
        except Exception as e:
            print(f"Erro ao ler {file_path}: {e}")

    apps = sorted(apps, key=lambda a: a["name"].lower())
    return apps


# Chamada Direta Temporária Para Testar a Classe
if __name__ == "__main__":
    apps = get_linux_apps()
    for app in apps[:20]:
        print(f"{app['name']} -> {app['command']}")
    print(f"\nTotal: {len(apps)} aplicativos encontrados")
