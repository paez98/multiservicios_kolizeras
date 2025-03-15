import flet as ft
from tabs import tabs
from ui.cliente_ui import cargar_clientes_en_tabla


def main(page: ft.Page):
    # Configuración de la ventana
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.title = "Taller Mecánico App"
    page.window_width = 1000
    page.window_height = 600
    page.window_resizable = True  # Permite redimensionar
    page.bgcolor = "#1e1e1e"

    page.add(tabs)

    cargar_clientes_en_tabla()


if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
