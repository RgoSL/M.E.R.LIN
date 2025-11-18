from customtkinter import *
from PIL import Image


def criar_containers(
    parent, variavel, apps, largura=400, altura=60, cor_texto="#000000", callback=None
):
    for i, app in enumerate(apps):
        frame = CTkFrame(
            parent,
            corner_radius=10,
            fg_color="#FFFFFF",
            width=largura,
            height=altura,
            border_color="#C58ADE",
            border_width=2,
        )
        frame.grid(row=i, column=0, padx=100, pady=5)
        frame.grid_propagate(False)
        frame.grid_columnconfigure(1, weight=1)

        if "icon" in app and app["icon"]:
            try:
                img = CTkImage(dark_image=Image.open(app["icon"]), size=(28, 28))
                CTkLabel(frame, image=img, text="").grid(
                    row=0, column=0, padx=10, pady=10
                )
            except:
                CTkLabel(frame, text="❓").grid(row=0, column=0, padx=10, pady=10)
        else:
            CTkLabel(frame, text="❓").grid(row=0, column=0, padx=10, pady=10)

        CTkLabel(
            frame, text=app["name"], anchor="w", font=("Bold", 16), text_color=cor_texto
        ).grid(row=0, column=1, padx=10, sticky="w")

        rb = CTkRadioButton(
            frame,
            text="",
            value=app["name"],
            variable=variavel,
            fg_color="#654E82",
            command=lambda a=app: callback(a) if callback else None,
        )
        rb.grid(row=0, column=2, padx=10, sticky="e")
