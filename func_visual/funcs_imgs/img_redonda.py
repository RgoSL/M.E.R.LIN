from PIL import Image, ImageDraw, ImageOps, ImageFilter
from customtkinter import CTkLabel, CTkImage, CTkFrame
import os

def imagem_redonda(parent, caminho, tamanho, texto="", cor_fundo="transparent", espacamento_texto=10, comando=None):
    # Container para imagem + texto (sem usar pack com side="left")
    container = CTkFrame(parent, fg_color=cor_fundo, corner_radius=8)
    
    # Carrega e processa a imagem arredondada
    try:
        imagem = Image.open(caminho).convert("RGBA")
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
            bg_color=cor_fundo,
            corner_radius=tamanho//2
        )
        label_img.image = ctk_img  # Manter referência
        label_img.pack(pady=(10, espacamento_texto))
        
        # Label do texto
        if texto:
            label_texto = CTkLabel(
                container, 
                text=texto, 
                font=("Arial", 12), 
                text_color="white", 
                bg_color=cor_fundo
            )
            label_texto.pack(pady=(0, 10))
            
            # Bind do clique no texto também
            if comando:
                label_texto.bind("<Button-1>", lambda e: comando())
        
        # Bind do clique na imagem
        if comando:
            label_img.bind("<Button-1>", lambda e: comando())
            container.bind("<Button-1>", lambda e: comando())
    
    except Exception as e:
        print(f"Erro ao carregar imagem {caminho}: {e}")
        # Container de erro caso a imagem não carregue
        label_erro = CTkLabel(
            container,
            text=f"Erro\n{texto}" if texto else "Erro",
            font=("Arial", 10),
            text_color="red",
            bg_color=cor_fundo
        )
        label_erro.pack(expand=True, fill="both", padx=10, pady=10)
    
    return container


# Exemplo de uso corrigido para seu frame1:
def configurar_imagens_no_frame(frame1, controller):
    """
    Função auxiliar para organizar as imagens no frame scrollável
    """
    # Limpar frame anterior se necessário
    for widget in frame1.winfo_children():
        widget.destroy()
    
    # Container principal para as imagens
    container_imagens = CTkFrame(frame1, fg_color="transparent")
    container_imagens.pack(fill="both", expand=True, padx=60, pady=20)
    
    # Lista de imagens para facilitar a adição
    imagens_dados = [
        {"caminho": "assets/ImgsTemp/placeholder.jpg", "texto": "Item 1"},
        {"caminho": "assets/ImgsTemp/placeholder.jpg", "texto": "Item 2"},  
        {"caminho": "assets/ImgsTemp/placeholder.jpg", "texto": "Item 3"},
        {"caminho": "assets/ImgsTemp/placeholder.jpg", "texto": "Item 4"},
        {"caminho": "assets/ImgsTemp/placeholder.jpg", "texto": "Item 5"},
    ]
    
    # Adicionar imagens usando grid para melhor controle
    for i, dados in enumerate(imagens_dados):
        img_container = imagem_redonda(
            container_imagens,
            dados["caminho"],
            170,
            dados["texto"],
            "#654E82",
            espacamento_texto=8,
            comando=lambda: controller.mostrar_pagina("comandos_coletanea")
        )
        
        # Usar grid para posicionamento horizontal
        img_container.grid(
            row=0, 
            column=i, 
            padx=150, 
            pady=10, 
            sticky="n"
        )
        
        # Configurar peso da coluna para distribuição uniforme
        container_imagens.grid_columnconfigure(i, weight=0)
    
    # Coluna extra para empurrar tudo para a esquerda se necessário
    container_imagens.grid_columnconfigure(len(imagens_dados), weight=1)


# Uso simplificado no seu código principal:
# Substitua suas chamadas de imagem_redonda por:
# configurar_imagens_no_frame(frame1, self.controller)