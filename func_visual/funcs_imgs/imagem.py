from customtkinter import *
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps


def adicionar_imagem_texto(
    parent,
    caminho_img_dark=None,          # imagem para modo escuro
    caminho_img_light=None,    # imagem para modo claro (opcional)
    texto=" ",
    cor="transparent",
    tamanho=100,
    espacamento=30,
    cor_texto="#654E82",
    comando=None,
):

    container = CTkFrame(parent, fg_color=cor, corner_radius=8)

    try:
        # Se não houver imagem light, usa a mesma para ambos
        if caminho_img_light is None:
            caminho_img_light = caminho_img_dark

        # Carrega as duas imagens
        img_dark = Image.open(caminho_img_dark).convert("RGBA")
        img_light = Image.open(caminho_img_light).convert("RGBA")

        # Função para preparar imagem redonda
        def prepara(img):
            img = ImageOps.fit(img, (tamanho, tamanho), Image.Resampling.LANCZOS)

            # Criar máscara redonda com suavização
            scale = 4
            big_size = (tamanho * scale, tamanho * scale)
            mask = Image.new("L", big_size, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0) + big_size, fill=255)
            mask = mask.filter(ImageFilter.GaussianBlur(2))
            mask = mask.resize((tamanho, tamanho), Image.Resampling.LANCZOS)

            img.putalpha(mask)
            return img

        # Prepara ambas as imagens para ficarem com círculo suave
        img_dark = prepara(img_dark)
        img_light = prepara(img_light)

        # CTkImage agora com imagens diferentes para light/dark
        ctk_img = CTkImage(
            dark_image=img_dark,
            light_image=img_light,
            size=(tamanho, tamanho)
        )

        # Label da imagem
        label_img = CTkLabel(
            container,
            image=ctk_img,
            text="",
            bg_color=cor,
            corner_radius=tamanho // 2,
        )
        label_img.image = ctk_img
        label_img.pack(pady=(10, espacamento))

        # Label do texto
        label_texto = None
        if texto:
            label_texto = CTkLabel(
                container,
                text=texto,
                font=("Gideon Roman", 22),
                text_color=cor_texto,
                bg_color=cor,
            )
            label_texto.pack(pady=(0, 10))

        # Clique em toda a área
        if comando:
            container.bind("<Button-1>", lambda e: comando())
            label_img.bind("<Button-1>", lambda e: comando())
            if label_texto:
                label_texto.bind("<Button-1>", lambda e: comando())

    except Exception as e:
        print(f"Erro ao carregar imagem {caminho_img_dark}: {e}")

        label_erro = CTkLabel(
            container,
            text=f"Erro\n{texto}" if texto else "Erro",
            font=("Gideon Roman", 12),
            text_color="red",
            bg_color=cor,
        )
        label_erro.pack(expand=True, fill="both", padx=10, pady=10)

        if comando:
            container.bind("<Button-1>", lambda e: comando())

    return container
