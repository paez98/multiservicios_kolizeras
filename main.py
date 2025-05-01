import flet as ft
from faker import Faker
from logica.manejo_cliente import ManejoCliente
from logica.manejo_servicio import ManejoServicio
from tabs import tabs

manejo = ManejoCliente()
servicio = ManejoServicio()
fake = Faker()


def main(page: ft.Page):
    # Configuración de la ventana

    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.title = "Taller Mecánico App"
    page.theme = ft.Theme(font_family="Poppins")
    page.window_resizable = True  # Permite redimensionar
    # page.theme_mode = ft.ThemeMode.LIGHT
    page.add(tabs)
    page.update()


print("recargado")
if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
