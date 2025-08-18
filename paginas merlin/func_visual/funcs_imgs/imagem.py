from customtkinter import *
from PIL import Image, ImageOps, ImageDraw, ImageFilter

def adicionar_imagem_texto(parent, caminho_img, texto=" ", cor="transparent", 
                   tamanho=100, espacamento=30, cor_texto="white"):
    # Container para imagem + texto (sem usar pack com side="left")
    container = CTkFrame(parent, fg_color=cor, corner_radius=8)
    
    # Carrega e processa a imagem arredondada
    try:
        imagem = Image.open(caminho_img).convert("RGBA")
        imagem = ImageOps.fit(imagem, (tamanho, tamanho), Image.Resampling.LANCZOS)
        
        # Criar máscara circular com anti-aliasing
        scale = 4
        big_size = (tamanho * scale, tamanho * scale)
        mask = Image.new('L', big_size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + big_size, fill=255)
        mask = mask.filter(ImageFilter.GaussianBlur(2))
        mask = mask.resize((tamanho, tamanho), Image.Resampling.LANCZOS)
        
        imagem.putalpha(mask)
        
        # Criar objeto CTkImage
        ctk_img = CTkImage(dark_image=imagem, light_image=imagem, size=(tamanho, tamanho))
        
        # Label da imagem
        label_img = CTkLabel(
            container, 
            image=ctk_img, 
            text="", 
            bg_color=cor,
            corner_radius=tamanho//2
        )
        label_img.image = ctk_img  # Manter referência
        label_img.pack(pady=(10, espacamento))
        
        # Label do texto
        if texto:
            label_texto = CTkLabel(
                container, 
                text=texto, 
                font=("Arial", 12), 
                text_color=cor_texto, 
                bg_color=cor
            )
            label_texto.pack(pady=(0, 10))
            
            # Bind do clique no texto também
    
    except Exception as e:
        print(f"Erro ao carregar imagem {caminho_img}: {e}")
        # Container de erro caso a imagem não carregue
        label_erro = CTkLabel(
            container,
            text=f"Erro\n{texto}" if texto else "Erro",
            font=("Arial", 10),
            text_color="red",
            bg_color=cor
        )
        label_erro.pack(expand=True, fill="both", padx=10, pady=10)
    
    return container