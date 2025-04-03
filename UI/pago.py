import flet as ft
from utils.utils import crear_boton, crear_campo_texto
from logica.manejo_cliente import ManejoCliente

# ===============================================
#     ELEMENTOS DE LA INTERFAZ DE PAGOS
# ===============================================


class PagoUiState:
    def __init__(self) -> None:
        # Logica pagos
        self.manejo_cliente = ManejoCliente()

        # DropDown Components

        self.tittle = ft.Text(
            "Registro de pagos",
            text_align=ft.TextAlign.CENTER,
            size=30,
            color="#9C27B0",
        )
        self.dd_cliente = ft.Dropdown(
            enable_filter=True,
            editable=True,
            label="Cliente",
            width=250,
            options=[
                ft.dropdown.Option(cliente["nombre"])
                for cliente in self.manejo_cliente.cargar_nombre_clientes()
            ],
            border_color="#9C27B0",
        )

        self.dd_servicio = ft.Dropdown(
            enable_filter=True,
            label="Servicio",
            width=250,
            options=[
                ft.dropdown.Option("Cambio de aceite"),
                ft.dropdown.Option("Alineación"),
                ft.dropdown.Option("Frenos"),
            ],
            border_color="#9C27B0",
        )

        # DataTable de pagos
        self.lista_de_pago = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Nombre")),
                ft.DataColumn(ft.Text("Servicio")),
                ft.DataColumn(ft.Text("Monto")),
                ft.DataColumn(ft.Text("Fecha")),
            ],
            rows=[],
            expand=True,
            border=ft.border.all(1, ft.Colors.GREY_300),
        )

        self.txt_monto = crear_campo_texto("Monto")
        self.btn_registro = ft.ElevatedButton(
            text="Registrar Pago",
            icon=ft.Icons.PAYMENT,
            style=ft.ButtonStyle(
                bgcolor=ft.colors.PURPLE_300,
                padding=ft.padding.all(20),
            ),
        )


# region VISTA
def setup_pagos_ui(state: PagoUiState) -> ft.Control:
    """Retorna la interfaz grafica de la seccion de Pago"""
    return ft.Column(
        controls=[
            ft.Column(
                controls=[
                    state.tittle,
                    ft.ResponsiveRow(
                        controls=[
                            ft.Container(
                                content=state.dd_cliente,
                                col={"sm": 12, "md": 5, "lg": 3},
                                # padding=5,
                            ),
                            ft.Container(
                                content=state.dd_servicio,
                                col={"sm": 12, "md": 5, "lg": 3},
                                # padding=5,
                            ),
                            ft.Container(
                                content=state.txt_monto,
                                col={"sm": 12, "md": 5, "lg": 3},
                                # padding=5,
                            ),
                            ft.Container(
                                content=state.btn_registro,
                                col={"sm": 12, "md": 5, "lg": 3},
                                # padding=5,
                                alignment=ft.alignment.center,
                            ),
                        ],
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            ft.Divider(),
            ft.Container(
                content=ft.Column(
                    controls=[state.lista_de_pago],
                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                ),
                expand=True,
            ),
        ],
        expand=True,
    )


pago_state = PagoUiState()
vista_pagos = setup_pagos_ui(pago_state)
