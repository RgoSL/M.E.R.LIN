from customtkinter import *
from PIL import Image
import os

from func_visual.imagem import adcionar_imagem


class config(CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        # Frame roxo de fundo total
        frame = CTkFrame(self, fg_color="#FFFFFF", corner_radius=0)
        frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        # header

        header = CTkFrame(self, fg_color="#654E82", corner_radius=0)
        header.place(relx=0, rely=0, relwidth=1, relheight=0.1)

        label = CTkLabel(header, text="Escolha como se preparar", font=("Bold", 20), text_color="black")
        label.place(relx=0.5, rely=0.5, anchor=CENTER)

        Label2 = CTkLabel(self, text="Tipo de Configuração:", font=("Bold", 18), text_color="black",bg_color="white")
        Label2.place(relx=0.62, rely=0.35, anchor=CENTER)

        radio_var = IntVar()

        # Primeira opção
        frame_check = CTkFrame(self, fg_color="white", corner_radius=15, border_color="#C58ADE", border_width=2,bg_color="white")
        frame_check.place(relx=0.7, rely=0.45, relwidth=0.4, relheight=0.13, anchor=CENTER)

        radio1 = CTkRadioButton(frame_check, text="Opção 1", font=("Bold", 15), text_color="black",
                                variable=radio_var, value=1, fg_color="#654E82")
        radio1.place(relx=0.2, rely=0.5, anchor=CENTER)

        # Segunda opção
        frame_check2 = CTkFrame(self, fg_color="white", corner_radius=15, border_color="#C58ADE", border_width=2,bg_color="white")
        frame_check2.place(relx=0.7, rely=0.6, relwidth=0.4, relheight=0.13, anchor=CENTER)

        radio2 = CTkRadioButton(frame_check2, text="Opção 2", font=("Bold", 15), text_color="black",
                                variable=radio_var, value=2, fg_color="#654E82")
        radio2.place(relx=0.2, rely=0.5, anchor=CENTER)

        # Botões
        btn_voltar = CTkButton(self, text="Voltar", font=("Bold", 15), text_color="white", fg_color="#654E82",corner_radius=10, command=lambda: controller.mostrar_pagina("inicial"), hover=False)
        
        btn_proximo = CTkButton(self, text="Proximo",  font=("Bold", 15), text_color="white", fg_color="#654E82",corner_radius=10,command=lambda: controller.mostrar_pagina("ajustes"), hover=False)
        
        btn_voltar.place(relx=0.15, rely=0.9, anchor=CENTER, relwidth=0.2, relheight=0.06)
        btn_proximo.place(relx=0.85, rely=0.9, anchor=CENTER, relwidth=0.2, relheight=0.06)

        # Barra de progresso
        progress_bar = CTkProgressBar(self, mode="determinate", width=200, height=20,
                                      fg_color="#654E82", progress_color="#C58ADE")
        progress_bar.place(relx=0.5, rely=0.9, anchor=CENTER, relwidth=0.4, relheight=0.03)

         # DEBUG: Vamos investigar os caminhos
        print("=== DEBUG CAMINHOS ===")
        print(f"__file__ = {__file__}")
        print(f"Diretório atual: {os.getcwd()}")
        
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        print(f"Base dir calculado: {base_dir}")
        
        logo_path = os.path.join(base_dir, "func_visual", "logo.png")
        print(f"Caminho da logo: {logo_path}")
        print(f"Arquivo existe? {os.path.exists(logo_path)}")
        
        # Vamos também testar outros caminhos possíveis
        alternative_paths = [
            "func_visual/logo.png",
            "./func_visual/logo.png",
            os.path.join(os.getcwd(), "func_visual", "logo.png"),
            "../func_visual/logo.png"
        ]
        
        print("\n=== TESTANDO CAMINHOS ALTERNATIVOS ===")
        for path in alternative_paths:
            print(f"{path} -> Existe: {os.path.exists(path)}")
        
        print("\n=== LISTANDO ARQUIVOS ===")
        try:
            func_visual_dir = os.path.join(base_dir, "func_visual")
            if os.path.exists(func_visual_dir):
                print(f"Arquivos em func_visual: {os.listdir(func_visual_dir)}")
            else:
                print("Diretório func_visual não encontrado!")
                
            # Listar arquivos do diretório atual
            print(f"Arquivos no diretório raiz: {os.listdir(base_dir)}")
        except Exception as e:
            print(f"Erro ao listar arquivos: {e}")
        
        print("=== FIM DEBUG ===\n")
        
        # Tentar carregar a imagem com o caminho que funciona
        logo_loaded = False
        for path in [logo_path] + alternative_paths:
            if os.path.exists(path):
                try:
                    print(f"Tentando carregar imagem de: {path}")
                    adcionar_imagem(self, path, 0.12, 0.3, self, padx=10, pady=60,
                                   texto_str="A sua História começa aqui", cor="#FFFFFF",corF="white")
                    print("✓ Imagem carregada com sucesso!")
                    logo_loaded = True
                    break
                except Exception as e:
                    print(f"✗ Erro ao carregar imagem de {path}: {e}")
        
        if not logo_loaded:
            print("⚠ Criando fallback text label")
            # Fallback: label de texto
            fallback_label = CTkLabel(self, text="🖼 A sua História começa aqui", 
                                    font=("Bold", 16), text_color="#654E82",
                                    bg_color="white")
            fallback_label.place(relx=0.12, rely=0.12, anchor="nw")