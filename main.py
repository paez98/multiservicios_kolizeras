import flet as ft
from tabs import tabs
from ui.cliente_ui import _cargar_clientes
from logica.manejo_cliente import ManejoCliente
from faker import Faker

# from ui.cliente_ui import cargar_clientes_en_tabla
majeo = ManejoCliente()
fake = Faker()


def main(page: ft.Page):
    # Configuración de la ventana
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.title = "Taller Mecánico App"
    page.window_width = 1000
    page.window_height = 600
    page.window_resizable = True  # Permite redimensionar
    page.theme_mode = ft.ThemeMode.DARK
    # page.bgcolor = "#1e1e1e"
    page.add(tabs)
    page.update()


if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
