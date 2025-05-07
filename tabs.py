import flet as ft
import time
from ui.home import home, actualizar_dashboard, carga_tabla_ordenes
from ui.orders import container_ordenes_ui
from ui.cliente_ui import vista_clientes, _cargar_clientes, cliente_state
from ui.servicios import lista_servicios, _cargar_servicio, servicio_state
from ui.pago import vista_pagos, _cargar_pagos, pago_state
from ui.orders import cargar_orden

clientes_cargados = False
servicios_cargados = False
pagos_cargados = False
dashboard_cargado = False
ordenes_cargadas = False


def cargar_datos_pestana(e):
    global clientes_cargados, servicios_cargados, pagos_cargados, dashboard_cargado, ordenes_cargadas
    tab_index = e.control.selected_index

    # if tab_index == 0 and not dashboard_cargado:
    #     inicio_timer_dashboard = time.time()
    #     carga_tabla_ordenes()
    #     actualizar_dashboard(e)
    #     dashboard_cargado = True
    #     fin_timer_dash = time.time()
    #     print(
    #         f"El tiempo de ejecucion de cargado del dash es {fin_timer_dash - inicio_timer_dashboard}"
    #     )

    if tab_index == 0 and not clientes_cargados:
        inicio_timer_clientes = time.time()
        _cargar_clientes(e, cliente_state)
        clientes_cargados = True
        fin_timer_clientes = time.time()
        print(
            f"El tiempo de ejecucion de carga de clientes es{fin_timer_clientes - inicio_timer_clientes}"
        )
    elif tab_index == 1 and not servicios_cargados:
        inicio_timer_servicios = time.time()
        _cargar_servicio(e, servicio_state)
        servicios_cargados = True
        fin_timer_servicios = time.time()
        print(
            f"El tiempo de ejecucion de carga de servicios es {fin_timer_servicios - inicio_timer_servicios} "
        )
    elif tab_index == 2 and not ordenes_cargadas:
        inicio_timer_ordenes = time.time()
        cargar_orden(e)
        ordenes_cargadas = True
        fin_timer_ordenes = time.time()
        print(
            f"El tiempo de ejecucion de carga de ordenes es{fin_timer_ordenes - inicio_timer_ordenes} "
        )

    elif tab_index == 3 and not pagos_cargados:
        inicio_timer_pagos = time.time()
        _cargar_pagos(e, pago_state)
        pagos_cargados = True
        fin_timer_pagos = time.time()
        print(
            f"El tiempo de ejecucion de carga de pagos {fin_timer_pagos - inicio_timer_pagos}"
        )


tabs = ft.Tabs(
    selected_index=0,
    animation_duration=300,
    tabs=[
        ft.Tab(
            text="DashBoard",
            icon=ft.Icons.HOME,
            content=home,
        ),
        ft.Tab(text="Clientes", icon=ft.Icons.PEOPLE_ALT, content=vista_clientes),
        ft.Tab(
            text="Servicios",
            icon=ft.Icon(ft.Icons.DESIGN_SERVICES),
            content=lista_servicios,
        ),
        ft.Tab(text="Ordenes", icon=ft.Icons.SUMMARIZE, content=container_ordenes_ui),
        ft.Tab(
            text="Pago",
            icon=ft.Icons.ATTACH_MONEY,
            content=vista_pagos,
        ),
    ],
    on_change=cargar_datos_pestana,
    tab_alignment=ft.TabAlignment.CENTER,
    padding=200,
    expand=True,
    unselected_label_color=ft.Colors.GREY_800,
)
