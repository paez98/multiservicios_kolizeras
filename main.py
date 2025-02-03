import flet as ft
from UI.cliente_ui import lista_clientes
from tabs import tabs


def main(page: ft.Page):
    # Configuración de la ventana
    page.title = "Taller Mecánico App"
    page.window_width = 1000
    page.window_height = 600
    page.window_resizable = True  # Permite redimensionar
    page.theme_mode = ft.ThemeMode.LIGHT
    tabs
    page.add(tabs)


if __name__ == '__main__':
    ft.app(target=main)
