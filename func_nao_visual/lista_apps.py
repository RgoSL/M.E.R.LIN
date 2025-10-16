# Import das Bibliotecas Utilizadas
from customtkinter import *
import subprocess

# Import da Função que Busca Pelos Apps no Windows
from scripts.windows.buscar_apps import *  

# Criação da Classe de Execução
class AppList(CTkFrame):
    def __init__(self, master, apps):
        super().__init__(master, fg_color = "#654E82")
        self.apps = apps
        self.filtered_apps = apps
        self.show_favorites = False

        top_frame = CTkFrame(self, fg_color = "#654E82")
        top_frame.pack(fill = "x", pady = 5)
        
# Barra de Pesquisa no Começo
        self.search_var = StringVar()
        search_entry = CTkEntry(top_frame, text_color = "#d9d9d9", border_color = "#F9B14F", textvariable = self.search_var)
        search_entry.pack(side = "left", fill = "x", expand = True, padx = 10)
        search_entry.bind("<KeyRelease>", self.update_list)
        
# Botão do Canto Superior Direito
        self.toggle_button = CTkButton(top_frame, text = "Favoritos ⭐", width = 100, fg_color = "#432D5D", hover_color = "#C58ADE", text_color = "#F9B14F", command = self.toggle_favorites)
        self.toggle_button.pack(side = "right", padx = 10)

        self.scroll_frame = CTkScrollableFrame(self, fg_color = "#654E82", label_text = "Aplicativos", label_fg_color = "#200B3A", scrollbar_button_color = "#F9B14F")
        self.scroll_frame.pack(fill = "both", expand = True, padx = 10, pady = 5)

        self.populate_list()

    def populate_list(self):
        
# Botões ao Lado dos Aplicativos
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        for app in self.filtered_apps:
            app_frame = CTkFrame(self.scroll_frame, fg_color = "#3A205A", corner_radius = 10)
            app_frame.pack(fill = "x", pady = 5, padx = 5)

            label = CTkLabel(app_frame, text = app["name"], anchor = "w")
            label.pack(side = "left", padx = 10, pady = 5, fill = "x", expand = True)

            fav_button = CTkButton(
                app_frame,
                text = "⭐" if app["favorite"] else "☆",
                width = 40,
                fg_color = "#432D5D",
                hover_color = "#C58ADE",
                text_color = "#F9B14F",
                command = lambda a = app: self.toggle_favorite(a)
            )
            fav_button.pack(side = "right", padx = 5)

            open_button = CTkButton(app_frame, text = "Abrir", width = 60, fg_color = "#432D5D", hover_color = "#C58ADE", command = lambda c = app["command"]: self.open_app(c))
            open_button.pack(side = "right", padx = 5)
            
# Lógica do Controle de Favoritos
    def update_list(self, event = None):
        query = self.search_var.get().lower()
        if self.show_favorites:
            self.filtered_apps = [a for a in self.apps if a["favorite"] and query in a["name"].lower()]
        else:
            self.filtered_apps = [a for a in self.apps if query in a["name"].lower()]
        self.populate_list()

    def toggle_favorite(self, app):
        app["favorite"] = not app["favorite"]
        self.update_list()

    def toggle_favorites(self):
        self.show_favorites = not self.show_favorites
        self.toggle_button.configure(
            text = "Todos 📋" if self.show_favorites else "Favoritos ⭐"
        )
        self.update_list()

    def open_app(self, command):
        try:
            subprocess.Popen(command, shell=True)
        except Exception as e:
            print(f"Erro ao abrir {command}: {e}")

# Lista de Aplicativos Encontrados no Sistema
apps = get_windows_apps()

# Criando a Tela de Exibição da Lista
def abrir_lista_apps(master):
    ListaApps = CTkToplevel(master)
    ListaApps.geometry("400x600+100+100")
    ListaApps.title("Lista de Aplicativos - M.E.R.LIN")
    ListaApps.iconbitmap("images\\logo.png")
    ListaApps.wm_attributes("-topmost", True)  
    app_list = AppList(ListaApps, apps)
    app_list.pack(fill = "both", expand = True, padx = 10, pady = 10) 