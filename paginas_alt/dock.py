# Bibliotecas Utilizadas
import os
import threading
from customtkinter import *
from PIL import Image

# Métodos Específicos Para Bloquear Logs
os.environ["GLOG_minloglevel"] = "3"
os.environ["ABSL_LOGGING"] = "0"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

import time

# Imports Das Funcionalidades Presentes na Dock
from func_nao_visual.comandos_dock import btns
from func_nao_visual.lista_apps import (abrir_lista_apps, carregar_apps_em_thread)
from func_visual.modos.sistema_cores import cores
from eye_tracking.track_central import gerenciador, calcular_posicao_nariz

class Dock(CTkToplevel):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.cores = cores()

        # Definindo o ID de Cliente da Dock
        self.cliente_id = "dock"

        # Confirmar e Força o Foco
        self.after(50, self.focus_force)
        self.after(100, self.lift)
        self.after(120, lambda: self.attributes("-topmost", True))

        # Atrasos nos Tempos de Execução em Relação ao Detectar
        self.cooldown_tab = 0.6
        self.cooldown_enter = 0.6
        self.ultimo_tab = 0
        self.ultimo_enter = 0

        # Debugs
        self.tempo_direita = 0
        self.tempo_esquerda = 0

        # Botões
        self.botoes_dock = []
        self.botao_selecionado = 0

        # Estilização
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.wm_attributes("-transparentcolor", self.cores["transparente"])

        # Posicionamento da Dock
        altura_tela = self.winfo_screenheight()
        largura_tela = self.winfo_screenwidth()
        largura_dock = 80
        altura_dock = 446
        offset = 55
        dock_x = largura_tela - largura_dock
        dock_y = altura_tela - altura_dock - offset
        self.geometry(f"{largura_dock}x{altura_dock}+{dock_x}+{dock_y}")

        # Frame Principal
        self.Frame = CTkFrame(
            self,
            bg_color=self.cores["transparente"],
            fg_color=self.cores["fundo_frame"],
            border_width=2,
            border_color=self.cores["borda_destaque"],
            corner_radius=10,
        )
        self.Frame.pack(fill="both", expand=True)

        # Método Para Criar os Botões
        self._criar_botoes()

        # Navegação
        def atualizar_selecao():
            for i, botao in enumerate(self.botoes_dock):
                if i == self.botao_selecionado:
                    botao.configure(
                        border_width=2,
                        border_color=self.cores["borda_destaque"]
                    )
                else:
                    botao.configure(border_width=0)

        def navegar(event=None):
            self.botao_selecionado = (self.botao_selecionado + 1) % len(
                self.botoes_dock
            )
            atualizar_selecao()
            return "break"

        def ativar(event=None):
            botao = self.botoes_dock[self.botao_selecionado]
            botao.invoke()
            return "break"

        atualizar_selecao()

        self.bind("<Tab>", navegar)
        self.bind("<Return>", ativar)
        self.bind("<FocusIn>", self._on_focus_in)
        self.bind("<FocusOut>", self._on_focus_out)
        self.focus_set()

        self.func_navegar = navegar
        self.func_ativar = ativar
        self.func_atualizar_selecao = atualizar_selecao

        # Registro da Dock Como um Cliente
        gerenciador.registrar_cliente(
            self.cliente_id,
            self._processar_deteccao,
            ativo=True
        )

        self.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _criar_botoes(self):
        # Cria o Padrão Dos Botões da Dock
        def btns_dock(caminho, command=None):
            Btn = Image.open(caminho)
            Btn = Btn.resize((150, 120))
            Btn = CTkImage(light_image=Btn, dark_image=Btn)

            Bot = CTkButton(
                self.Frame,
                image=Btn,
                text="",
                width=60,
                height=60,
                fg_color=self.cores["botao_normal"],
                hover_color=self.cores["hover"],
                corner_radius=10,
                command=command,
            )
            Bot.image = Btn
            Bot.pack(pady=8)

            self.botoes_dock.append(Bot)
            return Bot

        btns_dock("assets/ImgsDock/LApps.png",
                 command=lambda: carregar_apps_em_thread(self))
        btns_dock("assets/ImgsDock/pacotes.png",
                 command=lambda: btns.Btn_Pacotes(self.controller))
        btns_dock("assets/ImgsDock/navegador.png",
                 command=lambda: btns.Btn_Navegador())
        btns_dock("assets/ImgsDock/teclado.png",
                 command=lambda: btns.Btn_Teclado(self))
        btns_dock("assets/ImgsDock/ajustes.png",
                 command=lambda: btns.Btn_Ajustar(self.controller, "ajustes"))
        btns_dock("assets/ImgsDock/Fechar.png",
                 command=lambda: btns.Btn_Fechar(self))

    def _processar_deteccao(self, resultado):
        # Chamada da Função da Classe Central de Detecção
        landmarks = resultado.get("landmarks")
        if not landmarks:
            return

        w = resultado["width"]
        h = resultado["height"]
        agora = time.time()

        # Cálculo da Posição em que Estamos Olhando
        nariz_x = calcular_posicao_nariz(landmarks, w, h)

        # Detecção do Nariz Para o Lado Direito
        if nariz_x >= 0.50:
            self.tempo_direita += 1
            self.tempo_esquerda = 0
        # Detecção do Nariz Para o Lado Esquerdo
        elif nariz_x <= 0.38:
            self.tempo_esquerda += 1
            self.tempo_direita = 0
        # Centro - reseta contadores
        else:
            # Ativação do Tab Para Seleção
            if (self.tempo_direita > 6 and
                (agora - self.ultimo_tab) > self.cooldown_tab):
                
                if self.focus_displayof() == self:
                    self.after(0, self.func_navegar)
                self.after(50, self.focus_force)
                self.ultimo_tab = agora
                
            # Ativação do Enter Para Execução
            elif (self.tempo_esquerda > 6 and
                  (agora - self.ultimo_enter) > self.cooldown_enter):
                
                if self.focus_displayof() == self:
                    self.after(0, self.func_ativar)
                self.after(50, self.focus_force)
                self.ultimo_enter = agora

            self.tempo_direita = 0
            self.tempo_esquerda = 0

    def _on_focus_in(self, event=None):
        # Detecção Ativada na Hora do Foco
        gerenciador.ativar_cliente(self.cliente_id)
        print(f"🎯 Dock em foco")

    def _on_focus_out(self, event=None):
        # Detecção Desativada Quando não Houver Foco
        gerenciador.desativar_cliente(self.cliente_id)
        print(f"Dock sem foco")

    def atualizar_tema(self):
        self.cores = cores()
        self.wm_attributes("-transparentcolor", self.cores["transparente"])
        self.Frame.configure(
            fg_color=self.cores["fundo_frame"],
            border_color=self.cores["borda_destaque"]
        )
        for botao in self.botoes_dock:
            botao.configure(
                fg_color=self.cores["botao_normal"],
                hover_color=self.cores["hover"]
            )
        self.func_atualizar_selecao()
        print(f"Dock atualizada para tema: {get_appearance_mode()}")

    def _on_closing(self):
        # Remove a Dock Dos Clientes Salvos ao Fechar
        gerenciador.remover_cliente(self.cliente_id)
        self.destroy()