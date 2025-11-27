import os
from customtkinter import *

from func_nao_visual.Banco.preferencias import (carregar_ajustes, criar_tabela, salvar_ajustes)
from func_visual.widgets.header import nav
from func_visual.widgets.progress import progress_bar
from func_visual.widgets.i18n import i18n

from PIL import Image

class ajustes(CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        criar_tabela()

        nav(self, controller, "M.E.R.LIN")

        self.titulo = CTkLabel(
            self, 
            text=i18n.t("titulo_ajustes"), 
            font=("Gideon Roman", 30), 
            text_color="#654E82"
        )
        self.titulo.place(relx=0.5, rely=0.2, anchor=CENTER)

        frame2 = CTkFrame(self, fg_color="#654E82", corner_radius=20)
        frame2.place(relx=0.5, rely=0.62, relwidth=0.82, relheight=0.58, anchor=CENTER)
        self.frame2 = frame2

        dados = carregar_ajustes()
        if dados:
            resolucao_sel, idioma_sel, fps_sel, luz_sel = dados
        else:
            resolucao_sel = "1080p"
            idioma_sel = self.obter_nome_idioma_atual() 
            fps_sel = "60 fps"
            luz_sel = "Sim"

        menu_h = 0.12
        menu_w = 0.20
        fonte_itens = ("Arial", 17)

        opt_cfg = {
            "fg_color": "#E6C8FA",
            "dropdown_fg_color": "#654E82",
            "text_color": "black",
            "button_hover_color": "#56397C",
            "button_color": "#E6C8FA",
            "font": fonte_itens,
        }

        self.OptionMenu5 = CTkOptionMenu(
            frame2, 
            values=[], 
            command=self.salvar_config_camera,
            **opt_cfg
        )
        self.OptionMenu5.set(luz_sel)
        self.OptionMenu5.place(
            relx=0.23, rely=0.27, anchor=W, relwidth=menu_w, relheight=menu_h
        )

        self.OptionMenu1 = CTkOptionMenu(
            frame2, 
            values=[], 
            command=self.salvar_config_camera,
            **opt_cfg
        )
        self.OptionMenu1.set(resolucao_sel)
        self.OptionMenu1.place(
            relx=0.47, rely=0.27, anchor=W, relwidth=menu_w, relheight=menu_h
        )

        self.OptionMenu3 = CTkOptionMenu(
            frame2, 
            values=[], 
            command=self.salvar_config_camera,
            **opt_cfg
        )
        self.OptionMenu3.set(fps_sel)
        self.OptionMenu3.place(
            relx=0.71, rely=0.27, anchor=W, relwidth=menu_w, relheight=menu_h
        )

        self.OptionMenu2 = CTkOptionMenu(
            frame2, 
            values=[], 
            command=self.ao_mudar_idioma,
            **opt_cfg
        )
        self.OptionMenu2.set(idioma_sel)
        self.OptionMenu2.place(
            relx=0.23, rely=0.48, anchor=W, relwidth=0.68, relheight=menu_h
        )

        self.atualizar_option_menus()

        self.label_camera = CTkLabel(
            frame2, 
            text=i18n.t("ajuste_camera"), 
            font=("Arial", 17), 
            text_color="#E6C8FA"
        )
        self.label_camera.place(relx=0.12, rely=0.23, anchor=W)

        self.label_lingua = CTkLabel(
            frame2, 
            text=i18n.t("ajuste_lingua"), 
            font=("Arial", 17), 
            text_color="#E6C8FA"
        )
        self.label_lingua.place(relx=0.12, rely=0.44, anchor=W)

        self.label_termos = CTkLabel(
            frame2,
            text=i18n.t("ajuste_termos"),
            font=("Arial", 16),
            text_color="#E6C8FA",
            cursor="hand2",
        )
        self.label_termos.place(relx=0.15, rely=0.9, anchor=CENTER)
        self.label_termos.bind(
            "<Button-1>", lambda e: self.controller.mostrar_pagina("termos_de_uso")
        )

        self.barra = progress_bar(
            self, cor_progresso="#C58ADE", modo="determinate", valor=1
        )
        self.barra.place(relx=0.5, rely=0.95, anchor=CENTER)

        icone_voltar = CTkImage(
            Image.open("assets/ImgsTemp/seta_esquerda.png"), size=(26, 26)
        )
        icone_avanc = CTkImage(
            Image.open("assets/ImgsTemp/seta_direita.png"), size=(26, 26)
        )

        btn_voltar = CTkButton(
            self,
            image=icone_voltar,
            text="",
            fg_color="#654E82",
            hover_color="#56397C",
            width=50,
            height=50,
            command=lambda: controller.mostrar_pagina("modo_claro_escuro"),
        )
        btn_voltar.place(relx=0.07, rely=0.20, anchor=CENTER)

        avanc = CTkButton(
            self,
            image=icone_avanc,
            text="",
            fg_color="#654E82",
            hover_color="#56397C",
            width=50,
            height=50,
            command=lambda: controller.mostrar_pagina("inicial"),
        )
        avanc.place(relx=0.9, rely=0.20, anchor=CENTER)

    def obter_nome_idioma_atual(self):

        mapeamento = {
            "pt": i18n.t("ajustes_idiomas1"), 
            "en": i18n.t("ajustes_idiomas2"),  
            "es": i18n.t("ajustes_idiomas3"), 
        }
        return mapeamento.get(i18n.idioma_atual, i18n.t("ajustes_idiomas1"))

    def obter_codigo_idioma(self, nome_idioma):

        mapeamentos = {
            "Português": "pt",
            "Portuguese": "pt",
            "Portugués": "pt",
            
            "Inglês": "en",
            "English": "en",
            "Inglés": "en",
            
            "Espanhol": "es",
            "Spanish": "es",
            "Español": "es",
        }
        
        return mapeamentos.get(nome_idioma, "pt")

    def atualizar_option_menus(self):
        valores_luz = [i18n.t("ajustes_cam"), i18n.t("ajustes_sim"), i18n.t("ajustes_nao")]
        self.OptionMenu5.configure(values=valores_luz)
        
        valores_resolucao = [i18n.t("ajustes_res"), "1080p", "720p", "360p"]
        self.OptionMenu1.configure(values=valores_resolucao)
        
        valores_fps = ["FPS", "120 fps", "60 fps", "30 fps"]
        self.OptionMenu3.configure(values=valores_fps)
        
        # Valores para Idiomas - traduzidos
        valores_idiomas = [
            i18n.t("ajustes_idiomas1"),  
            i18n.t("ajustes_idiomas2"),  
            i18n.t("ajustes_idiomas3")   
        ]
        self.OptionMenu2.configure(values=valores_idiomas)

    def ao_mudar_idioma(self, nome_idioma_selecionado):

        codigo_idioma = self.obter_codigo_idioma(nome_idioma_selecionado)
        
        print(f"Mudando idioma via ajustes: {nome_idioma_selecionado} -> {codigo_idioma}")
        
        self.controller.mudar_idioma_manual(codigo_idioma)
        
        self.salvar_config_camera()

    def atualizar_idioma(self):
        self.titulo.configure(text=i18n.t("titulo_ajustes"))
        
        self.label_camera.configure(text=i18n.t("ajuste_camera"))
        self.label_lingua.configure(text=i18n.t("ajuste_lingua"))
        self.label_termos.configure(text=i18n.t("ajuste_termos"))
        
        self.atualizar_option_menus()
        
        idioma_atual_nome = self.obter_nome_idioma_atual()
        self.OptionMenu2.set(idioma_atual_nome)
        
        print(f"Página ajustes atualizada para idioma: {i18n.idioma_atual}")

    def salvar_config_camera(self, _=None):
        import json
        import os
        
        resolucao = self.OptionMenu1.get()
        fps = self.OptionMenu3.get()
        luz = self.OptionMenu5.get()
        
        idioma_nome = self.OptionMenu2.get()
        
        salvar_ajustes(resolucao, idioma_nome, fps, luz)
        
        try:
            config_path = "config/preferencias.json"
            os.makedirs(os.path.dirname(config_path), exist_ok=True)
            
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
            else:
                config = {}
            
            config['resolucao'] = resolucao
            config['fps'] = fps
            config['luz_camera'] = luz
            
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
            
            print(f"Configurações de câmera salvas: Resolução={resolucao}, FPS={fps}, Luz={luz}")
            
        except Exception as e:
            print(f"Erro ao salvar configurações no JSON: {e}")

    def atualizar_info_label(self):
        pass