import flet as ft


home = ft.Container(
    image_src='taller.png',
    image_fit=ft.ImageFit.COVER,
    image_opacity=0.3,  # Opacidad de la imagen (0 a 1)
    expand=True,
    border=ft.border.all(2, '#bbdefb')
)
