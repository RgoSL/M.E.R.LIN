import ctypes
import json
import os
import locale

from customtkinter import *

from paginas_alt.ajustes import ajustes
from paginas_alt.comandos_coletanea import comandos_coletanea
from paginas_alt.esc_config import config
from paginas_alt.esc_so import configSo
from paginas_alt.idioma_software import idioma_software
from paginas_alt.impressao import bemVindo
from paginas_alt.inicial import inicial
from paginas_alt.modo_claro_escuro import modo_claro_escuro
from paginas_alt.termos_de_uso import termos_de_uso
from paginas_alt.video_assis import video_Assis

from func_visual.widgets.i18n import i18n

def centralizar_janela(janela, largura, altura):
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()
    x = int((largura_tela / 2) - (largura / 2))
    y = int((altura_tela / 2) - (altura / 2))
    janela.geometry(f"{largura}x{altura}+{x}+{y}")

def cor_atual():
    modo = get_appearance_mode()
    return "#FFFFFF" if modo == "Light" else "#2B2B2B"
class App(CTk):
    def __init__(self):
        super().__init__()

        self.carregar_idioma_inicial()

        set_appearance_mode("dark")
        self.largura_janela = 800
        self.altura_janela = 600
        self.radius = 30
        centralizar_janela(self, self.largura_janela, self.altura_janela)
        self.configure(fg_color="#2B2B2B")
        self.overrideredirect(True)
        self.app_selecionado = None
        self.after(100, self.arredondar_janela)

        self.main_frame = CTkFrame(self, fg_color="#2B2B2B", corner_radius=self.radius)
        self.main_frame.pack(expand=True, fill="both")

        self.title_bar = CTkFrame(self.main_frame, height=30, fg_color="#1E1E1E")
        self.title_bar.pack(fill="x", side="top")

        self.title_label = CTkLabel(
            self.title_bar, text="M.E.R.LIN", fg_color="#1E1E1E"
        )
        self.title_label.pack(side="left", padx=10)

        i18n.registrar_observer(self)

        self.frames = {}
        pages = [
            bemVindo,
            idioma_software,
            configSo,
            config,
            modo_claro_escuro,
            ajustes,
            inicial,
            termos_de_uso,
            comandos_coletanea,
            video_Assis,
        ]
        
        for PageClass in pages:
            page_name = PageClass.__name__
            try:
                frame = PageClass(self.main_frame, self)
                self.frames[page_name] = frame
                frame.place(relx=0, rely=0, relwidth=1, relheight=1)
                
                if hasattr(frame, 'atualizar_idioma'):
                    i18n.registrar_observer(frame)
                    print(f"Página {page_name} registrada para atualizações de idioma")
                else:
                    print(f"Página {page_name} não possui método atualizar_idioma()")
                    
            except Exception as e:
                print(f"Erro ao inicializar página {page_name}: {e}")

        self.mostrar_pagina(pages[0].__name__)
        self.maximized = False

    def carregar_idioma_inicial(self):
        try:
            config_path = "config/preferencias.json"
            
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    idioma_salvo = config.get('idioma')
                    
                    if idioma_salvo and idioma_salvo in ['pt', 'en', 'es']:
                        i18n.mudar_idioma(idioma_salvo)
                        print(f"Idioma carregado das preferências: {idioma_salvo}")
                        return
            
            idioma_sistema = self.detectar_idioma_sistema()
            i18n.mudar_idioma(idioma_sistema)
            print(f"Idioma do sistema detectado: {idioma_sistema}")
            
        except Exception as e:
            print(f"Erro ao carregar idioma: {e}")
            i18n.mudar_idioma("pt")
            print("Usando idioma padrão: pt")
    
    def detectar_idioma_sistema(self):
        try:
            idioma_sistema = locale.getdefaultlocale()[0]
            
            if idioma_sistema:
                codigo = idioma_sistema[:2].lower()
                
                if codigo in ["pt", "en", "es"]:
                    return codigo
            
            return "pt"
            
        except Exception as e:
            print(f"Erro ao detectar idioma do sistema: {e}")
            return "pt"

    def arredondar_janela(self):
        try:
            hwnd = ctypes.windll.user32.GetParent(self.winfo_id())
            region = ctypes.windll.gdi32.CreateRoundRectRgn(
                0,
                0,
                self.largura_janela + 1,
                self.altura_janela + 1,
                self.radius,
                self.radius,
            )
            ctypes.windll.user32.SetWindowRgn(hwnd, region, True)
        except Exception as e:
            print("Erro ao arredondar a janela:", e)

    def mostrar_pagina(self, nome):
        if nome in self.frames:
            self.frames[nome].tkraise()
            print(f"Mostrando página: {nome}")
        else:
            print(f"Página '{nome}' não encontrada!")

    def atualizar_idioma(self):
        self.title_label.configure(text=i18n.t("titulo_app"))
        print(f"App principal atualizada para idioma: {i18n.idioma_atual}")

    def atualizar_tema(self):
        modo = get_appearance_mode()
        if modo == "Light":
            nova_cor = "#FFFFFF"
        else:
            nova_cor = "#2B2B2B"

        for frame in self.frames.values():
            try:
                frame.configure(fg_color=nova_cor)
            except:
                pass

        self.main_frame.configure(fg_color=nova_cor)
        self.title_bar.configure(fg_color="#1E1E1E")

    def aplicar_tema_personalizado(self):
        modo = get_appearance_mode()

        if modo == "Light":
            bg_cor = "#FFFFFF"
            texto_cor = "#000000"
        else:
            bg_cor = "#2B2B2B"
            texto_cor = "#FFFFFF"

        self.configure(fg_color=bg_cor)
        self.main_frame.configure(fg_color=bg_cor)

        for frame in self.frames.values():
            try:
                frame.configure(fg_color=bg_cor)
                for widget in frame.winfo_children():
                    try:
                        widget.configure(fg_color=bg_cor, text_color=texto_cor)
                    except:
                        pass
            except:
                pass

    def mudar_idioma_manual(self, codigo_idioma):
        if codigo_idioma in ['pt', 'en', 'es']:
            i18n.mudar_idioma(codigo_idioma)
            self.salvar_preferencia_idioma(codigo_idioma)
            print(f"Idioma alterado para: {codigo_idioma}")
        else:
            print(f"Idioma '{codigo_idioma}' não suportado")

    def salvar_preferencia_idioma(self, codigo_idioma):
        try:
            config_path = "config/preferencias.json"
            
            os.makedirs(os.path.dirname(config_path), exist_ok=True)
            
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
            else:
                config = {}
            
            config['idioma'] = codigo_idioma
            
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
                
            print(f"Preferência de idioma salva: {codigo_idioma}")
            
        except Exception as e:
            print(f"Erro ao salvar preferência de idioma: {e}")

    def __del__(self):
        try:
            i18n.remover_observer(self)
            for frame in self.frames.values():
                if hasattr(frame, 'atualizar_idioma'):
                    i18n.remover_observer(frame)
        except:
            pass

if __name__ == "__main__":
    app = App()
    app.mainloop()