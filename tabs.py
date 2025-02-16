import flet as ft

from ui.cliente_ui import vista_clientes
from servicios import lista_servicios
from home import home
from pago import pago_container

tabs = ft.Tabs(
    selected_index=0,
    animation_duration=300,
    tabs=[
        ft.Tab(
            text="Home",
            icon=ft.Icons.HOME,
            content=home,
        ),
        ft.Tab(text="Clientes", icon=ft.Icons.PEOPLE_ALT, content=vista_clientes),
        ft.Tab(
            text="Servicios",
            icon=ft.Icon(ft.Icons.DESIGN_SERVICES),
            content=ft.Container(lista_servicios),
        ),
        ft.Tab(
            text="Pago",
            icon=ft.Icons.ATTACH_MONEY,
            content=pago_container,
        ),
    ],
    expand=1,
)
