import os

from customtkinter import CTkFrame, CTkImage, CTkLabel
from PIL import Image, ImageDraw, ImageFilter, ImageOps

def imagem_redonda(
    parent,
    caminho,
    tamanho,
    texto="",
    cor_fundo="#FFFFFF",
    espacamento_texto=10,
    comando=None,
    borda=3, 
):
    container = CTkFrame(parent, fg_color=cor_fundo, corner_radius=8)

    try:
        imagem = Image.open(caminho).convert("RGBA")

        imagem = ImageOps.fit(
            imagem,
            (tamanho - borda * 2, tamanho - borda * 2),
            Image.Resampling.LANCZOS,
        )

        mask_img = Image.new("L", imagem.size, 0)
        draw_img = ImageDraw.Draw(mask_img)
        draw_img.ellipse(
            (0, 0, imagem.size[0], imagem.size[1]),
            fill=255
        )
        imagem.putalpha(mask_img)

        final_img = Image.new("RGBA", (tamanho, tamanho), (255, 255, 255, 0))
        draw_border = ImageDraw.Draw(final_img)

        draw_border.ellipse(
            (0, 0, tamanho, tamanho),
            fill="#F9B14F" 
        )

        final_img.paste(imagem, (borda, borda), imagem)

        ctk_img = CTkImage(
            light_image=final_img,
            dark_image=final_img,
            size=(tamanho, tamanho)
        )

        label_img = CTkLabel(
            container,
            image=ctk_img,
            text="",
            bg_color=cor_fundo,
            corner_radius=tamanho // 2,
        )
        label_img.image = ctk_img
        label_img.pack(pady=(10, espacamento_texto))

        if texto:
            label_texto = CTkLabel(
                container,
                text=texto,
                font=("Arial", 12),
                text_color="#C58ADE",
                bg_color=cor_fundo,
            )
            label_texto.pack(pady=(0, 10))

            if comando:
                label_texto.bind("<Button-1>", lambda e: comando())
                
        if comando:
            label_img.bind("<Button-1>", lambda e: comando())
            container.bind("<Button-1>", lambda e: comando())

    except Exception as e:
        print(f"Erro ao carregar imagem {caminho}: {e}")
        label_erro = CTkLabel(
            container,
            text=f"Erro\n{texto}" if texto else "Erro",
            font=("Arial", 10),
            text_color="red",
            bg_color=cor_fundo,
        )
        label_erro.pack(expand=True, fill="both", padx=10, pady=10)

    return container

def configurar_imagens_no_frame(frame1, controller):
    for widget in frame1.winfo_children():
        widget.destroy()

    container_imagens = CTkFrame(frame1, fg_color="transparent")
    container_imagens.pack(fill="both", expand=True, padx=60, pady=20)

    imagens_dados = [
        {"caminho": "assets/ImgsConfig/Icone1.png", "texto": "Pacote 1"},
        {"caminho": "assets/ImgsConfig/Icone2.png", "texto": "Pacote 2"},
        {"caminho": "assets/ImgsConfig/Icone3.png", "texto": "Pacote 3"},
        {"caminho": "assets/ImgsConfig/Icone4.png", "texto": "Pacote 4"},
        {"caminho": "assets/ImgsConfig/Icone5.png", "texto": "Pacote 5"},
    ]

    for i, dados in enumerate(imagens_dados):
        img_container = imagem_redonda(
            container_imagens,
            dados["caminho"],
            170,
            dados["texto"],
            "#654E82",
            espacamento_texto=8,
            comando=lambda: controller.mostrar_pagina("comandos_coletanea"),
        )

        img_container.grid(row=0, column=i, padx=150, pady=10, sticky="n")
        container_imagens.grid_columnconfigure(i, weight=0)

    container_imagens.grid_columnconfigure(len(imagens_dados), weight=1)