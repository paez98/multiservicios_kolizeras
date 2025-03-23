import flet as ft

from ui.cliente_ui import vista_clientes, _cargar_clientes, cliente_state
from servicios import lista_servicios
from home import home
from pago import pago_container

clientes_cargados = False


def cargar_clientes_pestana(e):
    global clientes_cargados
    if e.control.selected_index == 1 and not clientes_cargados:
        _cargar_clientes(e, cliente_state)
        clientes_cargados = True


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
            content=lista_servicios,
        ),
        ft.Tab(
            text="Pago",

            icon=ft.Icons.ATTACH_MONEY,
            content=pago_container,
        ),
    ],
    on_change=cargar_clientes_pestana,
    padding=50,
    expand=1,
)
