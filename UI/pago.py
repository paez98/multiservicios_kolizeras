import datetime
import flet as ft
from utils.utils import crear_campo_texto, crear_boton
from logica.manejo_cliente import ManejoCliente
from logica.manejo_servicio import ManejoServicio
from ui.servicios import ServicioUiState
# ===============================================
#     ELEMENTOS DE LA INTERFAZ DE PAGOS
# ===============================================


class PagoUiState:
    def __init__(self) -> None:
        # Logica pagos
        self.manejo_cliente = ManejoCliente()
        self.manejo_servicio = ManejoServicio()

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
            col={"sm": 12, "lg": 2},
            border_color="#9C27B0",
        )

        self.dd_servicio = ft.Dropdown(
            enable_filter=True,
            editable=True,
            label="Servicio",
            width=250,
            options=[
                # ft.dropdown.Option(servicio["descripcion"])
                # for servicio in self.manejo_servicio.cargar_servicios()
            ],
            border_color="#9C27B0",
            col={"sm": 12, "lg": 2},
        )

        # Seleccion de fecha
        self.fecha_de_pago = ft.DatePicker(current_date=datetime.date.today())
        self.btn_fecha = ft.ElevatedButton(
            "Seleccionar Fecha",
            icon=ft.icons.DATE_RANGE,
            on_click=self._abrir_date_picker,
            col={"sm": 12, "lg": 2},
            style=ft.ButtonStyle(
                bgcolor=ft.colors.PURPLE_300,
                padding=ft.padding.all(20),
            ),
        )

        self.btn_registro = ft.ElevatedButton(
            text="Registrar Pago",
            icon=ft.Icons.PAYMENT,
            style=ft.ButtonStyle(
                bgcolor=ft.colors.PURPLE_300,
                padding=ft.padding.all(20),
            ),
            col={"sm": 12, "lg": 2},
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

        self.txt_monto = ft.TextField(
            label="Monto",
            read_only=True,
            width=200,
            col={"sm": 12, "lg": 2},
        )
        self.txt_fecha = ft.TextField(
            label="Fecha",
            # value=str(datetime.date.today()),
            read_only=True,
            width=200,
            col={"sm": 12, "lg": 2},
        )

        self._cargar_servicios_dropdown()

    def _abrir_date_picker(self, e):
        """Abre el selector de fecha"""
        e.control.page.open(self.fecha_de_pago)

    def _cargar_servicios_dropdown(self):
        servicios = self.manejo_servicio.cargar_servicios()
        self.dd_servicio.options = [
            ft.dropdown.Option(
                print(servicio),
                text=servicio["descripcion"],
                data=servicio["precio"],  # Almacenamos el precio en el data
            )
            for servicio in servicios
        ]

    def actualizar_monto_servicio(self, e):
        """Actualiza el monto cuando se selecciona un servicio"""
        if self.dd_servicio.value:
            # Obtenemos el precio directamente del option seleccionado
            self.txt_monto.value = str(
                next(
                    option.data
                    for option in self.dd_servicio.options
                    if option.text == self.dd_servicio.value
                )
            )
            self.txt_monto.update()


# region VISTA
def setup_pagos_ui(state: PagoUiState) -> ft.Control:
    """Retorna la interfaz grafica de la seccion de Pago"""
    state.dd_servicio.on_change = state.actualizar_monto_servicio
    return ft.Column(
        controls=[
            ft.Column(
                controls=[
                    state.tittle,
                    ft.ResponsiveRow(
                        controls=[
                            state.dd_cliente,
                            state.dd_servicio,
                            state.txt_monto,
                            state.txt_fecha,
                            state.btn_fecha,
                            state.btn_registro,
                        ],
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
