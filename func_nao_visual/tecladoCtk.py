from customtkinter import *
from pyautogui import *
import time

class Teclado(ctk_tk):
    def __init__(self):
        super().__init__()
        self.title("Teclado M.E.R.LIN")
        self.resizable(False, False)

    # Layout/Caracteres do Teclado
    self.layout = [
        ['1', '2', '3', '4','5', '6', '7', '8', '9', '0', 'Excluir'],
        ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
        ['a', 's', 'd', 'f', 'g', 'h', 'j', 'i', 'k', 'l', 'Enter'],
        ['z', 'x', 'c', 'v', 'b', 'n', 'm', ',' , '.', 'Espaço']
    ]

    self.historico = []
    self.texto_digitado = ""

    self.entrada = CTkEntry(self, width = 60, font = ('Arial', 14))
    self.entrada.pack(padx = 10, pady = 5)

    btn_enviar = CTkButton(self, text = "Digitar Texto", width = 15, height = 2, font = ('Arial', 12) command = self.enviar)
    btn_enviar.pack(pady = 5)

    self.teclado_frame = CTkFrame(self)
    self.teclado_frame.pack(padx = 10, pady = 10)

    self.canvas = CTkCanvas(self.teclado_frame, highlightthickness = 0, bg = 'SystemButtonFace')
    self.canvas.grid(row = 0, column = 0, rowspan = 5, columnspan = 12, sticky = "nsew")
    self.canvas_rect_id = None

    self.btns = {}
    self.carregar_teclas(self.layout)

    self.bind("<Up>", lambda e: self.quadrante(0))
    self.bind("<Right>", lambda e: self.quadrante(1))
    self.bind("<Down>", lambda e: self.quadrante(2))
    self.bind("<Left>", lambda e: self.quadrante(3))
    self.bind("<Return", self.confirmar)

    self.focos()

def carregar_teclas(self, layout):
    self.canvas.delete("all")
    for widget in self.teclado_frame.winfo_children():
        if widget != self.canvas:
            widget.destroy()

    self.btns = {}

    row_offset = 0
    if layout != self.layout:
        btn_voltar.grid(row = 0, column = 0, columnspan = max(len(row) for row in layout) + 1, padx = 2, pady = 2, sticky = "ew")
        self.btns["Voltar"] = btn_voltar
        row_offset = 1

    for r_idx, linha in emunerate(layout):
        for c_idx, tecla in enumerate(linha):
            Btn = CTkButton(self.teclado_frame, text = tecla, width = 5, height = 2,
                            command = lambda t = tecla: self.adicionar_a_entrada(t))
            Btn.grid(row = r_idx + row_offset, column = c_idx, padx = 2, pady = 2)
            self.btns[tecla] = Btn

    self.update_idletasks()
    bbox = self.teclado_frame.grid_bbox(0, 0, self.teclado_frame.grid_size()[0], self.teclado.grid_size()[1]) 
    if bbox:
        width = bbox[2] = bbox[0]
        height = bbox[3] - bbox[1]
        self.canvas.config(width = width, height = height)

    def desenhar_borda_quadrante(self, layout_quadradante):
        self.canvas.delete(self.canvas_react_id)

        if not layout_quadradante or not self.btns:
            self.canvas_react = None
            return
        
        tecla01 = layout_quadradante[0][0]
        linhaF = layout_quadradante[-1]
        teclaF = linhaF[-1]

        if tecla01 not in self.btns or teclaF not in self.btns:
            self.canvas_react_id = None
            return
        
        Btn01 = self.btns[tecla01]
        BtnF = self.btns[teclaF]