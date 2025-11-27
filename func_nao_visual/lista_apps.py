import subprocess
import threading
import time

from customtkinter import *
from scripts.windows.buscar_apps import *
from func_nao_visual.tecladoCtk import TecladoVarreduraTab
from func_visual.modos.sistema_cores import cores
from eye_tracking.track_central import gerenciador, eye_aspect_ratio

class AppList(CTkFrame):
    def __init__(self, master, apps):
        super().__init__(master, fg_color="transparent")
        
        self.cores = cores()
        self.cliente_id = f"applist_{id(self)}"
        
        self.apps = apps
        self.filtered_apps = apps
        self.show_favorites = False
        self.debounce_job = None

        self.ultimo_widget_focado = None

        self.itens_navegaveis = []
        self.index_atual = 0
        self.janela_teclado = None

        self.cooldown_tab = 0.4
        self.cooldown_enter = 0.4
        self.ultimo_tab = 0
        self.ultimo_enter = 0
        self.both_closed_start = None
        self.right_closed_start = None
        
        self.LEFT_EYE = [33, 160, 158, 133, 153, 144]
        self.RIGHT_EYE = [362, 385, 387, 263, 373, 380]
        
        self.criar_barra_superior()
        self.criar_lista_apps()

        self.bind("<FocusIn>", self._on_focus_in, add="+")
        self.bind("<FocusOut>", self._on_focus_out, add="+")
        
        gerenciador.registrar_cliente(
            self.cliente_id,
            self._processar_deteccao,
            ativo=False
        )

    def criar_barra_superior(self):
        top_frame = CTkFrame(self, fg_color=self.cores["fundo_frame"])
        top_frame.pack(fill="x", pady=5)

        self.search_var = StringVar()
        self.search_entry = CTkEntry(
            top_frame,
            text_color=self.cores["texto_principal"],
            fg_color=self.cores["fundo_secundario"],
            border_color=self.cores["borda_principal"],
            textvariable=self.search_var,
        )
        self.search_entry.pack(side="left", fill="x", expand=True, padx=10)
        self.search_entry.bind("<KeyRelease>", self.update_list)
        self.search_entry.bind("<FocusIn>", self.ativar_teclado)
        self.search_entry.bind("<Button-1>", self._focar_campo_pesquisa)

        self.toggle_button = CTkButton(
            top_frame,
            text="Favoritos ⭐",
            width=100,
            fg_color=self.cores["botao_normal"],
            hover_color=self.cores["hover"],
            text_color=self.cores["texto_destaque"],
            command=self.toggle_favorites,
        )
        self.toggle_button.pack(side="right", padx=10)

    def criar_lista_apps(self):
        self.scroll_frame = CTkScrollableFrame(
            self,
            fg_color=self.cores["fundo_frame"],
            label_text="Aplicativos",
            label_fg_color=self.cores["fundo_card"],
            label_text_color=self.cores["texto_principal"],
            scrollbar_button_color=self.cores["scrollbar"],
            scrollbar_button_hover_color=self.cores["scrollbar_hover"],
        )
        self.scroll_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.populate_list()

    def _processar_deteccao(self, resultado):
        landmarks = resultado.get("landmarks")
        if not landmarks:
            self.both_closed_start = None
            self.right_closed_start = None
            return

        w = resultado["width"]
        h = resultado["height"]
        now = time.time()

        # Calcula EAR
        left_ear = eye_aspect_ratio(landmarks, self.LEFT_EYE, w, h)
        right_ear = eye_aspect_ratio(landmarks, self.RIGHT_EYE, w, h)

        both_closed = (
            right_ear < 0.20 and left_ear < 0.20
        )

        # Com os Dois Olhos Fechados dá Tab
        if both_closed:
            if self.both_closed_start is None:
                self.both_closed_start = now
            elif now - self.both_closed_start >= 0.25:
                if now - self.ultimo_tab >= self.cooldown_tab:
                    self.after(0, self._navegar)
                    self.ultimo_tab = now
                    self.both_closed_start = None
        else:
            self.both_closed_start = None

        # Com o Olho Direito Fechado ele dá Enter
        if right_ear < 0.20 and left_ear >= 0.20:
            if self.right_closed_start is None:
                self.right_closed_start = now
            elif now - self.right_closed_start >= 0.50:
                if now - self.ultimo_enter >= self.cooldown_enter:
                    self.after(0, self._ativar)
                    self.ultimo_enter = now
                    self.right_closed_start = None
        else:
            self.right_closed_start = None

    def _on_focus_in(self, event=None):
        # O Foco Deve Estar no Frame e não no Input Para Ativar
        if event is None or event.widget != self.search_entry:
            gerenciador.ativar_cliente(self.cliente_id)
            print(f"AppList em foco")

    def _on_focus_out(self, event=None):
        gerenciador.desativar_cliente(self.cliente_id)
        print(f"AppList sem foco")

    def atualizar_tema(self):
        self.cores = cores()
        
        self.search_entry.configure(
            text_color=self.cores["texto_principal"],
            fg_color=self.cores["fundo_secundario"],
            border_color=self.cores["borda_principal"]
        )
        
        self.toggle_button.configure(
            fg_color=self.cores["botao_normal"],
            hover_color=self.cores["hover"],
            text_color=self.cores["texto_destaque"]
        )
        
        self.scroll_frame.configure(
            fg_color=self.cores["fundo_frame"],
            label_fg_color=self.cores["fundo_card"],
            label_text_color=self.cores["texto_principal"],
            scrollbar_button_color=self.cores["scrollbar"],
            scrollbar_button_hover_color=self.cores["scrollbar_hover"]
        )
        
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

        if self.janela_teclado is None or not self.janela_teclado.winfo_exists():
            self.janela_teclado = TecladoVarreduraTab()

            if widget_dest is not None:
                try:
                    self.janela_teclado.widget_destino = widget_dest
                except Exception as e:
                    print(f"Erro ao setar widget destino: {e}")

            self.janela_teclado.protocol("WM_DELETE_WINDOW", self.fechar_teclado)
        else:
            if widget_dest is not None:
                try:
                    self.janela_teclado.widget_destino = widget_dest
                except Exception:
                    pass
            try:
                self.janela_teclado.focus_force()
            except Exception:
                pass

    def fechar_teclado(self):
        self.janela_teclado = None

    def populate_list(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        self.itens_navegaveis.clear()

        for idx, app in enumerate(self.filtered_apps):
            app_frame = CTkFrame(
                self.scroll_frame,
                fg_color=self.cores["fundo_card"],
                corner_radius=10
            )
            app_frame.pack(fill="x", pady=5, padx=5)

            label = CTkLabel(
                app_frame,
                text=app["name"],
                anchor="w",
                text_color=self.cores["texto_principal"]
            )
            label.pack(side="left", padx=10, pady=5, fill="x", expand=True)

            fav_button = CTkButton(
                app_frame,
                text="⭐" if app["favorite"] else "☆",
                width=40,
                fg_color=self.cores["botao_normal"],
                hover_color=self.cores["hover"],
                text_color=self.cores["texto_destaque"],
                command=self.criar_toggle_callback(app),
            )
            fav_button.pack(side="right", padx=5)

            open_button = CTkButton(
                app_frame,
                text="Abrir",
                width=60,
                fg_color=self.cores["botao_normal"],
                hover_color=self.cores["hover"],
                text_color=self.cores["texto_botao"],
                command=self.criar_open_callback(app["command"]),
            )
            open_button.pack(side="right", padx=5)

            self.itens_navegaveis.append({
                "frame": app_frame,
                "callback": self.criar_open_callback(app["command"]),
            })

        if self.itens_navegaveis:
            self._destacar_item(0)

    def _destacar_item(self, index):
        for i, item in enumerate(self.itens_navegaveis):
            if i == index:
                item["frame"].configure(
                    border_width=2,
                    border_color=self.cores["borda_destaque"]
                )
                try:
                    item["frame"].tkraise()
                except:
                    pass
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
        pass

    def __del__(self):
        try:
            gerenciador.remover_cliente(self.cliente_id)
        except:
            pass

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
    ListaApps.geometry("400+600+100+100")
    ListaApps.title("Lista de Aplicativos - M.E.R.LIN")
    ListaApps.wm_attributes("-topmost", True)
    
    c = cores()
    ListaApps.configure(fg_color=c["fundo_principal"])
    
    app_list = AppList(ListaApps, apps)
    app_list.pack(fill="both", expand=True, padx=10, pady=10)
    
    ListaApps.bind("<Tab>", lambda e: app_list._navegar())
    ListaApps.bind("<Return>", lambda e: app_list._ativar())
    
    ListaApps.after(50, ListaApps.focus_force)
    ListaApps.after(100, lambda: app_list.focus_set())