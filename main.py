import flet as ft
from ui.registro_ui import RegistroUI
from tabs import tabs


def main(page: ft.Page):
    # Configuración de la ventana
    page.title = "Taller Mecánico App"
    page.window_width = 1000
    page.window_height = 600
    page.window_resizable = True  # Permite redimensionar
    page.theme_mode = ft.ThemeMode.LIGHT
    tabs
    open_registro_dialog = RegistroUI(page)
    btn_abrir_registro = ft.ElevatedButton(
        text="Registrar Cliente",
        icon=ft.icons.PERSON_ADD,
        width=200,
        height=50,
        style=ft.ButtonStyle(bgcolor="#2196F3", color="white"),
        on_click=open_registro_dialog
    )
    page.add(tabs)


if __name__ == '__main__':
    ft.app(target=main)
