import flet as ft
from tabs import tabs
from logica.manejo_cliente import ManejoCliente
from logica.manejo_servicio import ManejoServicio
from faker import Faker


# from ui.cliente_ui import cargar_clientes_en_tabla
majeo = ManejoCliente()
servicio = ManejoServicio()
fake = Faker()


# class Contenedor(ft.Container):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)


# mi_contenedor = Contenedor(bgcolor="red", expand=True)
# mi_contenedor.content = vista_clientes


def main(page: ft.Page):
    # Configuración de la ventana
    def page_resize(e):
        size_text = f"{page.width} px"
        size_text.update()

    size_text = ft.Text(bottom=50, right=50, style="displaySmall")
    page.overlay.append(size_text)
    page.on_resize = page_resize
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.title = "Taller Mecánico App"
    page.window_width = 1000
    page.window_height = 600
    page.window_resizable = True  # Permite redimensionar
    page.theme_mode = ft.ThemeMode.DARK
    page.add(tabs)
    page.update()

    # for i in range(20):
    #     servicio.guardar_servicio(fake.name(), fake.pricetag())


if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
