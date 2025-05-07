import flet as ft
from tabs import tabs
from faker import Faker
from logica.manejo_cliente import ManejoCliente

fake = Faker()

clientes = ManejoCliente()


def main(page: ft.Page):
    # Configuración de la ventana
    # for i in range(10):
    #     clientes.guardar_cliente(
    #         nombre=fake.name(),
    #         telefono=fake.pho
    #         ne_number(),
    #         direccion=fake.address(),
    #     )

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
