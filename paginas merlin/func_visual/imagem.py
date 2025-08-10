from customtkinter import *
from PIL import Image

def adcionar_imagem(frame, caminho_img, relx, rely, janela, padx=50, pady=20, texto_str=" ", cor="white", corF="transparent"):
    """
    Versão corrigida que usa .place() ao invés de .pack()
    para ser compatível com o resto do código
    """
    try:
        # Definir tamanho fixo da imagem (você pode ajustar)
        largura = 200  # pixels
        altura = 160   # pixels

        # Carregar e redimensionar a imagem
        img_pil = Image.open(caminho_img).convert("RGBA")
        img_pil = img_pil.resize((largura, altura), Image.Resampling.LANCZOS)
        img_ctk = CTkImage(light_image=img_pil, size=(largura, altura))

        # Container para imagem e texto usando place()
        container = CTkFrame(frame, fg_color=cor, corner_radius=0,bg_color=corF)
        container.place(relx=relx, rely=rely, anchor="nw")

        # Label da imagem
        img_label = CTkLabel(container, image=img_ctk, text="", bg_color="white")
        img_label.image = img_ctk  # Manter referência
        img_label.pack(side="top", padx=10, pady=(10, 5))

        # Texto abaixo da imagem
        if texto_str and texto_str.strip():
            texto = CTkLabel(container, text=texto_str, font=("Arial", 12), 
                           text_color="black", fg_color="transparent", 
                           justify="center")
            texto.pack(side="top", padx=10, pady=(0, 10))
        else:
            texto = None

        return img_label, texto
        
    except Exception as e:
        print(f"Erro na função adcionar_imagem: {e}")
        import traceback
        traceback.print_exc()
        return None, None