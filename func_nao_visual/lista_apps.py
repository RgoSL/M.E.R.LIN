# Import das Bibliotecas Utilizadas
from customtkinter import *
import subprocess
import threading
import time

# Import da Função que Busca Pelos Apps no Windows
from scripts.windows.buscar_apps import *

# Import da Classe com o Teclado
from func_nao_visual.tecladoCtk import *

# Criação da Classe de Execução
class AppList(CTkFrame):
    def __init__(self, master, apps):
        super().__init__(master, fg_color="#654E82")
        self.apps = apps
        self.filtered_apps = apps
        self.show_favorites = False
        self.debounce_job = None  

        # Frame Superior
        top_frame = CTkFrame(self, fg_color="#654E82")
        top_frame.pack(fill="x", pady=5)

        # Barra de Pesquisa
        self.search_var = StringVar()
        search_entry = CTkEntry(top_frame, text_color="#d9d9d9", border_color="#F9B14F", textvariable=self.search_var)
        search_entry.pack(side="left", fill="x", expand=True, padx=10)
        search_entry.bind("<KeyRelease>", self.update_list)
        search_entry.bind("<FocusIn>", self.ativar_teclado)

        # Botão Favoritos
        self.toggle_button = CTkButton(
            top_frame,
            text="Favoritos ⭐",
            width=100,
            fg_color="#432D5D",
            hover_color="#C58ADE",
            text_color="#F9B14F",
            command=self.toggle_favorites
        )
        self.toggle_button.pack(side="right", padx=10)

        # Área de Rolagem com a Lista de Apps
        self.scroll_frame = CTkScrollableFrame(
            self,
            fg_color="#654E82",
            label_text="Aplicativos",
            label_fg_color="#200B3A",
            scrollbar_button_color="#F9B14F"
        )
        self.scroll_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.populate_list()

    def populate_list(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        # Criar widgets para cada app
        for app in self.filtered_apps:
            app_frame = CTkFrame(self.scroll_frame, fg_color="#3A205A", corner_radius=10)
            app_frame.pack(fill="x", pady=5, padx=5)

            label = CTkLabel(app_frame, text=app["name"], anchor="w")
            label.pack(side="left", padx=10, pady=5, fill="x", expand=True)

            fav_button = CTkButton(
                app_frame,
                text="⭐" if app["favorite"] else "☆",
                width=40,
                fg_color="#432D5D",
                hover_color="#C58ADE",
                text_color="#F9B14F",
                command=self.criar_toggle_callback(app)
            )
            fav_button.pack(side="right", padx=5)

            open_button = CTkButton(
                app_frame,
                text="Abrir",
                width=60,
                fg_color="#432D5D",
                hover_color="#C58ADE",
                command=self.criar_open_callback(app["command"])
            )
            open_button.pack(side="right", padx=5)

    # Debounce Para Bloquear as Sugestões da Barra
    def update_list(self, event=None):
        if self.debounce_job:
            self.after_cancel(self.debounce_job)
        self.debounce_job = self.after(300, self._perform_filter)

    # Executa o filtro da busca
    def _perform_filter(self):
        query = self.search_var.get().lower()

        if self.show_favorites:
            filtrado = [a for a in self.apps if a["favorite"] and query in a["name"].lower()]
        else:
            filtrado = [a for a in self.apps if query in a["name"].lower()]

        if filtrado != self.filtered_apps:
            self.filtered_apps = filtrado
            self.populate_list()

    def toggle_favorite(self, app):
        app["favorite"] = not app["favorite"]
        self._perform_filter()

    def toggle_favorites(self):
        self.show_favorites = not self.show_favorites
        self.toggle_button.configure(
            text="Todos 📋" if self.show_favorites else "Favoritos ⭐"
        )
        self._perform_filter()

    def open_app(self, command):
        try:
            if isinstance(command, list):
                subprocess.Popen(command, shell=False)
            else:
                subprocess.Popen(command, shell=True)
        except Exception as e:
            print(f"Erro ao abrir {command}: {e}")

    def criar_toggle_callback(self, app):
        return lambda: self.toggle_favorite(app)

    def criar_open_callback(self, command):
        return lambda: self.open_app(command)

    def ativar_teclado(self, event=None):
        if hasattr(self, 'teclado') and self.teclado.winfo_exists():
            self.teclado.destroy()

# Função Para Usar as Threads
def carregar_apps_em_thread(master):
    def run():
        try:
            apps = get_windows_apps()
            master.after(0, lambda: abrir_lista_apps(master, apps))
        except Exception as e:
            print(f"Erro ao carregar apps: {e}")
    threading.Thread(target=run, daemon=True).start()

# Criação da Janela de Lista
def abrir_lista_apps(master, apps):
    ListaApps = CTkToplevel(master)
    ListaApps.geometry("400x600+100+100")
    ListaApps.title("Lista de Aplicativos - M.E.R.LIN")
    ListaApps.iconbitmap("images\\logo.png")
    ListaApps.wm_attributes("-topmost", True)
    app_list = AppList(ListaApps, apps)
    app_list.pack(fill="both", expand=True, padx=10, pady=10)
