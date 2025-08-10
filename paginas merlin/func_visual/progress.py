import time
from paginas_alt.inicial import inicial

def avancar_para_inicial(App,progress_bar):
    progress_bar.set(0.4)
    App.update_idletasks()
    time.sleep(0.3)
    inicial()

    