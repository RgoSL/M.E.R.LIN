from customtkinter import CTk
from paginas_alt.inicial import inicial
from paginas_alt.esc_config import config
from paginas_alt.video_assis import video_Assis
from paginas_alt.ajustes import ajustes

class App(CTk):
    def __init__(self):
        super().__init__()
        self.geometry("800x600")
        self.title("Minha Aplicação")
        self.resizable(False, False)
        
        # Dicionário para guardar as páginas
        self.frames = {}

        # Instanciar todas as páginas e colocar no mesmo lugar
        for PageClass in (inicial, config, video_Assis, ajustes):
            page_name = PageClass.__name__
            frame = PageClass(self, self)
            self.frames[page_name] = frame
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.mostrar_pagina("inicial")

    def mostrar_pagina(self, nome):
        frame = self.frames[nome]
        frame.tkraise()

if __name__ == "__main__":
    app = App()
    app.mainloop()