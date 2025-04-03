import flet as ft


from ui.cliente_ui import vista_clientes, _cargar_clientes, cliente_state
from ui.servicios import lista_servicios, _cargar_servicio, servicio_state
from home import home
from ui.pago import vista_pagos

clientes_cargados = False
servicios_cargados = False


def cargar_datos_pestana(e):
    global clientes_cargados, servicios_cargados
    tab_index = e.control.selected_index
    if tab_index == 1 and not clientes_cargados:
        _cargar_clientes(e, cliente_state)
        clientes_cargados = True
    elif tab_index == 2 and not servicios_cargados:
        _cargar_servicio(e, servicio_state)
        servicios_cargados = True


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
            content=vista_pagos,
        ),
    ],
    on_change=cargar_datos_pestana,
    tab_alignment=ft.TabAlignment.CENTER,
    padding=200,
    expand=1,
    unselected_label_color=ft.Colors.GREY_800,
    scrollable=True,
)
