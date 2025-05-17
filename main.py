import flet as ft
from tabs import tabs
from logica.manejo_cliente import ManejoCliente

clientes = ManejoCliente()


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.title = "Taller Mecánico App"
    page.theme = ft.Theme(font_family="Poppins")
    page.window_resizable = True  # Permite redimensionar
    page.add(tabs)
    page.update()


print("recargado")
if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
