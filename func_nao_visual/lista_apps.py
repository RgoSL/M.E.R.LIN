import subprocess
import threading
import time

from customtkinter import *
from scripts.windows.buscar_apps import *
from func_nao_visual.tecladoCtk import *

from func_nao_visual.teclado_open import *

class AppList(CTkFrame):
    def __init__(self, master, apps):
        super().__init__(master, fg_color="#654E82")
        self.apps = apps
        self.filtered_apps = apps
        self.show_favorites = False
        self.debounce_job = None

        self.ultimo_widget_focado = None

        self.itens_navegaveis = []
        self.index_atual = 0
        self.janela = None 

        top_frame = CTkFrame(self, fg_color="#654E82")
        top_frame.pack(fill="x", pady=5)

        self.search_var = StringVar()
        search_entry = CTkEntry(
            top_frame,
            text_color="#d9d9d9",
            border_color="#F9B14F",
            textvariable=self.search_var,
        )
        search_entry.pack(side="left", fill="x", expand=True, padx=10)
        search_entry.bind("<KeyRelease>", self.update_list)
        search_entry.bind("<FocusIn>", self.ativar_teclado)

        search_entry.bind("<Button-1>", self._focar_campo_pesquisa) 

        self.toggle_button = CTkButton(
            top_frame,
            text="Favoritos ⭐",
            width=100,
            fg_color="#432D5D",
            hover_color="#C58ADE",
            text_color="#F9B14F",
            command=self.toggle_favorites,
        )
        self.toggle_button.pack(side="right", padx=10)

        self.scroll_frame = CTkScrollableFrame(
            self,
            fg_color="#654E82",
            label_text="Aplicativos",
            label_fg_color="#200B3A",
            scrollbar_button_color="#F9B14F",
        )
        self.scroll_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.populate_list()

    def _focar_campo_pesquisa(self, event=None):
        try:
            self.ultimo_widget_focado = event.widget
        except Exception:
            self.ultimo_widget_focado = None

        self.abrir_teclado_varredura(event)

    def abrir_teclado_varredura(self, event=None):
        widget_dest = None
        if event is not None and hasattr(event, "widget"):
            widget_dest = event.widget
        elif self.ultimo_widget_focado is not None:
            widget_dest = self.ultimo_widget_focado

        if self.janela is None or not self.janela.winfo_exists(): 
            self.janela = TecladoVarreduraTab() 

            if widget_dest is not None:
                try:
                    self.janela.widget_destino = widget_dest
                except Exception as e:
                    print("Erro ao setar widget_destino no teclado:", e)

            self.janela.protocol("WM_DELETE_WINDOW", self.fechar_janela)  
            self.janela.mainloop()  
        else:
            if widget_dest is not None:
                try:
                    self.janela.widget_destino = widget_dest
                except Exception as e:
                    print("Erro ao atualizar widget_destino no teclado:", e)
            try:
                self.janela.focus_force()
            except Exception:
                pass
            print("Teclado já está aberto.")

    def fechar_janela(self):
        self.janela = None
        print("Teclado fechado.")

    def populate_list(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        self.itens_navegaveis.clear()

        for idx, app in enumerate(self.filtered_apps):
            app_frame = CTkFrame(
                self.scroll_frame, fg_color="#3A205A", corner_radius=10
            )
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
                command=self.criar_toggle_callback(app),
            )
            fav_button.pack(side="right", padx=5)

            open_button = CTkButton(
                app_frame,
                text="Abrir",
                width=60,
                fg_color="#432D5D",
                hover_color="#C58ADE",
                command=self.criar_open_callback(app["command"]),
            )
            open_button.pack(side="right", padx=5)

            self.itens_navegaveis.append(
                {
                    "frame": app_frame,
                    "callback": self.criar_open_callback(app["command"]),
                }
            )

        self._destacar_item(0)

    def _destacar_item(self, index):
        for i, item in enumerate(self.itens_navegaveis):
            if i == index:
                item["frame"].configure(border_width=2, border_color="#F9B14F")
            else:
                item["frame"].configure(border_width=0)

    def _navegar(self, event=None):
        if len(self.itens_navegaveis) == 0:
            return "break"

        self.index_atual = (self.index_atual + 1) % len(self.itens_navegaveis)
        self._destacar_item(self.index_atual)
        return "break"

    def _ativar(self, event=None):
        if len(self.itens_navegaveis) == 0:
            return "break"

        item = self.itens_navegaveis[self.index_atual]
        item["callback"]()
        return "break"

    def update_list(self, event=None):
        if self.debounce_job:
            self.after_cancel(self.debounce_job)
        self.debounce_job = self.after(300, self._perform_filter)

    def _perform_filter(self):
        query = self.search_var.get().lower()

        if self.show_favorites:
            filtrado = [
                a for a in self.apps if a["favorite"] and query in a["name"].lower()
            ]
        else:
            filtrado = [a for a in self.apps if query in a["name"].lower()]

        if filtrado != self.filtered_apps:
            self.filtered_apps = filtrado
            self.index_atual = 0
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
        if hasattr(self, "teclado") and self.teclado.winfo_exists():
            self.teclado.destroy()

def carregar_apps_em_thread(master):
    def run():
        try:
            apps = get_windows_apps()
            master.after(0, lambda: abrir_lista_apps(master, apps))
        except Exception as e:
            print(f"Erro ao carregar apps: {e}")

    threading.Thread(target=run, daemon=True).start()

def abrir_lista_apps(master, apps):
    ListaApps = CTkToplevel(master)
    ListaApps.geometry("400x600+100+100")
    ListaApps.title("Lista de Aplicativos - M.E.R.LIN")
    ListaApps.wm_attributes("-topmost", True)
    app_list = AppList(ListaApps, apps)
    app_list.pack(fill="both", expand=True, padx=10, pady=10)
    ListaApps.bind("<Tab>", lambda e: app_list._navegar())
    ListaApps.bind("<Return>", lambda e: app_list._ativar())
    ListaApps.after(50, ListaApps.focus_force)