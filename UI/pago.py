import datetime
import flet as ft
from decimal import Decimal
from typing import Optional
from logica.logica_pago import LogicaPago
from logica.manejo_cliente import ManejoCliente
from logica.manejo_servicio import ManejoServicio
from tasa import usd_rate_simple


# ===============================================
#     ELEMENTOS DE LA INTERFAZ DE PAGOS
# ===============================================


class PagoUiState:
    def __init__(self) -> None:
        # Logica pagos
        self.manejo_cliente = ManejoCliente()
        self.manejo_servicio = ManejoServicio()
        self.manejo_pago = LogicaPago()

        self.monto_bolivares = None
        self.monto_usd_original: Optional[str] = None
        self.rate = usd_rate_simple

        self.tittle = ft.Text(
            "Registro de pagos",
            text_align=ft.TextAlign.CENTER,
            size=30,
            color="#9C27B0",
        )
        # ------Campos de texto--------

        self.txt_monto = ft.TextField(
            label="Monto",
            read_only=True,
            width=200,
            # prefix=ft.Text("$"),
            text_align=ft.TextAlign.RIGHT,
            col={"sm": 6, "lg": 1.5},
            border_color="#9C27B0",
        )

        self.txt_fecha = ft.TextField(
            label="Fecha",
            read_only=True,
            width=200,
            col={"sm": 12, "lg": 1.5},
            border_color="#9C27B0",
        )

        self.txt_referencia = ft.TextField(
            label="Referencia",
            width=200,
            col={"sm": 12, "lg": 1.5},
            border_color="#9C27B0",
            disabled=True,
        )

        # ------Dropdowns-----------
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

        self.dd_metodo = ft.Dropdown(
            label="Metodo",
            options=[ft.DropdownOption("Pagomovil"), ft.DropdownOption("$")],
            border_color="#9C27B0",
            col={"sm": 12, "lg": 1.5},
        )

        # Seleccion de fecha
        self.fecha_de_pago = ft.DatePicker(
            current_date=datetime.date.today(),
            on_change=lambda e: self._seleccionar_fecha(e),
        )
        # ------Botones------
        self.btn_fecha = ft.ElevatedButton(
            "Fecha",
            width=250,
            icon=ft.Icons.DATE_RANGE,
            on_click=self._abrir_date_picker,
            col={"sm": 12, "lg": 1.5},
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.PURPLE_300,
                padding=ft.padding.all(10),
            ),
        )

        self.btn_registro = ft.ElevatedButton(
            text="Registrar",
            width=250,
            icon=ft.Icons.PAYMENT,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.PURPLE_300,
                padding=ft.padding.all(10),
            ),
            on_click=lambda e: self._guardar_pagos(
                nombre=self.dd_cliente,
                servicio=self.dd_servicio,
                monto=self.txt_monto,
                referencia=self.txt_referencia,
                fecha=self.txt_fecha,
                page=e.page,
            ),
            col={"sm": 12, "lg": 1.5},
        )

        self.btn_actualizar = ft.ElevatedButton(
            text="Refresh",
            width=250,
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
                ft.DataColumn(ft.Text("Referencia")),
                ft.DataColumn(ft.Text("Fecha")),
            ],
            rows=[],
            expand=True,
            border=ft.border.all(1, ft.Colors.GREY_300),
        )
        self._cargar_clientes_dropdown()
        self._cargar_servicios_dropdown()

    # region METODOS

    def _abrir_date_picker(self, e):
        """Abre el selector de fecha"""
        e.control.page.open(self.fecha_de_pago)

    def _seleccionar_fecha(self, e):
        self.txt_fecha.value = f"{self.fecha_de_pago.value.strftime('%d-%m-%Y')}"

        e.control.page.update()

    @staticmethod
    def _validar_registro_pago(dd_cliente, dd_servicio, txt_fecha) -> dict:
        error = {}
        # Valdamos que haya un nombre seleccionado
        if not dd_cliente.value:
            error["nombre"] = "Selecciona un cliente"
        if not dd_servicio.value:
            error["servicio"] = "Selecciona un servicio"

        if not txt_fecha.value:
            error["fecha"] = "Selecciona una fecha"

        return error

    def _guardar_pagos(
        self, nombre, servicio, monto, referencia, fecha, page: Optional[ft.Page] = None
    ):
        errores = self._validar_registro_pago(
            dd_cliente=nombre, dd_servicio=servicio, txt_fecha=fecha
        )

        if errores:
            nombre.error_text = errores.get("nombre", "")
            servicio.error_text = errores.get("servicio", "")
            fecha.error_text = errores.get("fecha", "")
            nombre.update()
            servicio.update()
            fecha.update()
            return

        nombre_val = nombre.value
        servicio_val = servicio.value
        monto_val = f"{monto.prefix.value} {monto.value}"
        ref_val = referencia.value
        fecha_val = fecha.value

        print(
            f"Intentando guardar pago. Nombre: {nombre_val}, Servicio: {servicio_val}, Monto: {monto_val}, Fecha: {fecha_val}"
        )
        try:
            response = self.manejo_pago.guardar_pago(
                nombre_val, servicio_val, monto_val, ref_val, fecha_val
            )
            print(f"Pago guardado exitosamente {response}")

            # Limpiamos los campos
            print("Limpiando campos del formulario")
            nombre.value = None
            servicio.value = None
            monto.value = ""
            fecha.value = ""
            referencia.value = ""

            # Limpiamos los errores
            nombre.error_text = None
            servicio.error_text = None
            monto.error_text = None
            fecha.error_text = None

            nombre.update()
            servicio.update()
            monto.update()
            fecha.update()
            referencia.update()

            page.open(ft.SnackBar(ft.Text("¡Pago registrado con éxito!")))
            return response

        except Exception as e:
            print(f"Error al guardar el pago: {e}")
            page.open(
                ft.SnackBar(ft.Text(f"Error al guardar{e}"), bgcolor=ft.Colors.RED)
            )
            return None

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

        tasa_rate = Decimal(self.rate)
        if self.dd_servicio.value:
            # Obtenemos el precio directamente del option seleccionado
            self.monto_usd_original = str(
                next(
                    option.data
                    for option in self.dd_servicio.options
                    if option.text == self.dd_servicio.value
                )
            )

            monto_limpio = (
                self.monto_usd_original.replace("$", "")
                .replace(",", "")
                .replace(" ", "")
            )

            if self.dd_metodo.value == "Pagomovil":
                self.monto_bolivares = tasa_rate * Decimal(monto_limpio.strip())
                self.txt_monto.prefix = ft.Text("Bs.")
                self.txt_monto.value = f"{self.monto_bolivares:.2f}"
                self.txt_monto.update()
                self.txt_referencia.disabled = False
                self.txt_referencia.update()

                print(f"El monto en bs {self.monto_bolivares:.2f}")
            else:
                self.txt_monto.prefix = ft.Text("$")
                self.txt_monto.value = Decimal(monto_limpio.strip())
                self.txt_monto.update()
                self.txt_referencia.disabled = True
                self.txt_referencia.update()


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
                    ft.DataCell(ft.Text(pago["referencia"])),
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
    state.dd_metodo.on_change = state.actualizar_monto_servicio
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
                            state.dd_metodo,
                            state.txt_monto,
                            state.txt_referencia,
                            state.txt_fecha,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Row(
                        controls=[
                            state.btn_fecha,
                            state.btn_actualizar,
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
                    scroll=ft.ScrollMode.AUTO,
                ),
                expand=True,
            ),
        ],
        expand=True,
    )


pago_state = PagoUiState()
vista_pagos = setup_pagos_ui(pago_state)
