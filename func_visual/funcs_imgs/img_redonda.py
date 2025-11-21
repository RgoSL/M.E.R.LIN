import os

from customtkinter import CTkFrame, CTkImage, CTkLabel
from PIL import Image, ImageDraw, ImageFilter, ImageOps


def imagem_redonda(
    parent,
    caminho,
    tamanho,
    texto="",
    cor_fundo="transparent",
    espacamento_texto=10,
    comando=None,
):
    container = CTkFrame(parent, fg_color=cor_fundo, corner_radius=8)

    try:
        imagem = Image.open(caminho).convert("RGBA")
        imagem = ImageOps.fit(imagem, (tamanho, tamanho), Image.Resampling.LANCZOS)

        scale = 4
        big_size = (tamanho * scale, tamanho * scale)
        mask = Image.new("L", big_size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + big_size, fill=255)
        mask = mask.filter(ImageFilter.GaussianBlur(2))
        mask = mask.resize((tamanho, tamanho), Image.Resampling.LANCZOS)

        imagem.putalpha(mask)

        ctk_img = CTkImage(
            dark_image=imagem, light_image=imagem, size=(tamanho, tamanho)
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
                text_color="white",
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
        {"caminho": "assets/ImgsConfig/Icone1.png", "texto": "Item 1"},
        {"caminho": "assets/ImgsConfig/Icone2.png", "texto": "Item 2"},
        {"caminho": "assets/ImgsConfig/Icone3.png", "texto": "Item 3"},
        {"caminho": "assets/ImgsConfig/Icone4.png", "texto": "Item 4"},
        {"caminho": "assets/ImgsConfig/Icone5.png", "texto": "Item 5"},
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
