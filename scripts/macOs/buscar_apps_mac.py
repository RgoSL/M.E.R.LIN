# Essa Classe é Especifica Para Achar Apps no MacOS

# Bibliotecas Utilizadas na Classe
import os
import plistlib


def get_macos_apps(): # Função que Procura Pelos Apps
    app_dirs = [ # Definição dos Caminhos que Armazenam os Apps por Padrão em Sistemas Mac
        "/Applications",
        "/System/Applications",
        os.path.expanduser("~/Applications"),
        "/Applications/Utilities",
    ]

    apps = []
    seen = set()

    for directory in app_dirs:
        if not os.path.isdir(directory):
            continue

        for item in os.listdir(directory):
            if item.endswith(".app"):
                app_path = os.path.join(directory, item)
                plist_path = os.path.join(app_path, "Contents", "Info.plist")

                if not os.path.isfile(plist_path):
                    continue

                try:
                    with open(plist_path, "rb") as f:
                        info = plistlib.load(f)

                    # Método Para Encontrar os Nomes dos Programas
                    name = info.get("CFBundleDisplayName") or info.get("CFBundleName")
                    if not name:
                        name = item.replace(".app", "")

                    # Caminho que Armazena Executáveis do Mac
                    exec_name = info.get("CFBundleExecutable")
                    exec_path = os.path.join(
                        app_path, "Contents", "MacOS", exec_name
                    )

                    if name not in seen:
                        seen.add(name)
                        apps.append(
                            {
                                "name": name,
                                "command": f'"{exec_path}"',
                                "favorite": False,
                            }
                        )
                except Exception as e:
                    print(f"Erro ao ler {plist_path}: {e}")

    return sorted(apps, key=lambda x: x["name"].lower())