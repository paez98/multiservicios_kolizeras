import datetime
import flet as ft
from logica.logica_pago import LogicaPago
from logica.manejo_cliente import ManejoCliente
from logica.manejo_servicio import ManejoServicio
from ui.registro_ui import manejo_pago
from ui.servicios import ServicioUiState


# ===============================================
#     ELEMENTOS DE LA INTERFAZ DE PAGOS
# ===============================================


class PagoUiState:
    def __init__(self) -> None:
        # Logica pagos
        self.manejo_cliente = ManejoCliente()
        self.manejo_servicio = ManejoServicio()
        self.manejo_pago = LogicaPago()
        # DropDown Components

        self.tittle = ft.Text(
            "Registro de pagos",
            text_align=ft.TextAlign.CENTER,
            size=30,
            color="#9C27B0",
        )
        self.txt_monto = ft.TextField(
            label="Monto",
            read_only=True,
            width=200,
            col={"sm": 6, "lg": 1.5},
        )

        self.txt_fecha = ft.TextField(
            label="Fecha",
            # value=str(datetime.date.today()),
            read_only=True,
            width=200,
            col={"sm": 12, "lg": 1.5},
        )
        self.dd_cliente = ft.Dropdown(
            enable_filter=True,
            editable=True,
            label="Cliente",
            width=250,
            options=[],
            col={"sm": 12, "lg": 1.5},
            border_color="#9C27B0",
        )

        self.dd_servicio = ft.Dropdown(
            enable_filter=True,
            editable=True,
            label="Servicio",
            width=250,
            options=[],
            border_color="#9C27B0",
            col={"sm": 12, "lg": 1.5},
        )

        # Seleccion de fecha
        self.fecha_de_pago = ft.DatePicker(
            current_date=datetime.date.today(),
            on_change=lambda e: self._seleccionar_fecha(e),
        )
        self.btn_fecha = ft.ElevatedButton(
            "Fecha",
            icon=ft.Icons.DATE_RANGE,
            on_click=self._abrir_date_picker,
            col={"sm": 12, "lg": 1.5},
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.PURPLE_300,
                padding=ft.padding.all(10),
            ),
        )

        self.btn_registro = ft.ElevatedButton(
            text="Registrar Pago",
            icon=ft.Icons.PAYMENT,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.PURPLE_300,
                padding=ft.padding.all(10),
            ),
            on_click=lambda e: self._registrar_pago(
                self.dd_cliente.value,
                self.dd_servicio.value,
                self.txt_monto.value.strip(),
                self.txt_fecha.value.strip(),
            ),
            # on_click= lambda  e: manejo_pago.guardar_pago(self.dd_cliente.value,self.dd_servicio.value, self.txt_monto.value,self.txt_fecha.value.strip()),
            col={"sm": 12, "lg": 1.5},
        )

        self.btn_actualizar = ft.ElevatedButton(
            text="Refresh",
            icon=ft.Icons.REPLAY,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.PURPLE_300,
                padding=ft.padding.all(10),
            ),
            col={"sm": 12, "lg": 1.5},
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
        self._cargar_clientes_dropdown()
        self._cargar_servicios_dropdown()

    # region METODOS
    def _registrar_pago(self, nombre, servicio, monto, fecha):
        manejo_pago.guardar_pago(nombre, servicio, monto, fecha)

        self.dd_cliente.value = ""
        self.dd_servicio.value = ""
        self.txt_fecha.value = ""
        self.txt_monto.value = ""

        self.txt_monto.update()
        self.dd_servicio.update()
        self.dd_cliente.update()
        self.txt_fecha.update()

    def _abrir_date_picker(self, e):
        """Abre el selector de fecha"""
        e.control.page.open(self.fecha_de_pago)

    def _seleccionar_fecha(self, e):
        self.txt_fecha.value = f"{self.fecha_de_pago.value.strftime('%d-%m-%Y')}"

        e.control.page.update()

    def _cargar_servicios_dropdown(self):
        servicios = self.manejo_servicio.cargar_servicios()
        self.dd_servicio.options = [
            ft.dropdown.Option(
                text=servicio["descripcion"],
                data=servicio["precio"],  # Almacenamos el precio en el data
            )
            for servicio in servicios
        ]

    def _cargar_clientes_dropdown(self):
        clientes = self.manejo_cliente.cargar_clientes()
        self.dd_cliente.options = [
            ft.dropdown.Option(
                text=cliente["nombre"],
            )
            for cliente in clientes
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


# region LOGICA


def _cargar_pagos(e, state: PagoUiState):
    try:
        pagos = state.manejo_pago.cargar_pagos()
        state.lista_de_pago.rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(pago["nombre"])),
                    ft.DataCell(ft.Text(pago["servicio"])),
                    ft.DataCell(ft.Text(pago["monto"])),
                    ft.DataCell(ft.Text(pago["fecha"])),
                ]
            )
            for pago in pagos
        ]
        state.lista_de_pago.update()
    except Exception as e:
        print(f"Error al cargar los pagos {e}")


def _actualizar_todo(e, state: PagoUiState):
    _cargar_pagos(e, state)
    state.lista_de_pago.update()
    state._cargar_servicios_dropdown()
    state.dd_servicio.update()
    state._cargar_clientes_dropdown()
    state.dd_cliente.update()


# region VISTA
def setup_pagos_ui(state: PagoUiState) -> ft.Control:
    """Retorna la interfaz grafica de la seccion de Pago"""

    state.dd_servicio.on_change = state.actualizar_monto_servicio
    state.btn_actualizar.on_click = lambda e: _actualizar_todo(e, state)
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
                            state.btn_actualizar,
                            state.btn_registro,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
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
