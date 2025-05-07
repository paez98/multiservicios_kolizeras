import flet as ft

from decimal import Decimal
from tasa import usd_rate
from logica.manejo_cliente import ManejoCliente
from logica.logica_pago import LogicaPago
from logica.manejo_ordenes import ManejoOrdenes

manejo_ordenes = ManejoOrdenes()
manejo_cliente = ManejoCliente()
manejo_pagos = LogicaPago()

container_style = {
    "border_radius": 10,
    "padding": 5,
    "border": ft.border.all(1, ft.Colors.with_opacity(0.2, ft.Colors.ON_SURFACE)),
}


class TotalData(ft.Container):
    def __init__(self):
        super().__init__(
            **container_style,
        )
        self.txt_total_clientes = ft.Text("...", weight=ft.FontWeight.BOLD)

        self.content = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Card(
                            content=ft.Container(
                                content=ft.Column(
                                    controls=[
                                        ft.Icon(
                                            name=ft.Icons.CAR_REPAIR, color="amber"
                                        ),
                                        ft.Text("Carros totales"),
                                        ft.Text("Avg %", color="gold"),
                                    ],
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                                padding=10,
                                scale=1.0,
                                animate_scale=ft.Animation(
                                    300, ft.AnimationCurve.EASE_OUT
                                ),
                                on_click=lambda _: print("click card"),
                                on_hover=self.on_hover,
                            ),
                        ),
                        # Clientes de la semana
                        ft.Card(
                            content=ft.Container(
                                content=ft.Column(
                                    controls=[
                                        ft.Icon(
                                            name=ft.Icons.PERSON,
                                            color="amber",
                                        ),
                                        ft.Text("Clientes totales"),
                                        self.txt_total_clientes,
                                    ],
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                                padding=10,
                            ),
                        ),
                        # Ingresos de la semana
                        ft.Card(
                            content=ft.Container(
                                content=ft.Column(
                                    controls=[
                                        ft.Icon(name=ft.Icons.PERSON_ADD_ROUNDED),
                                        ft.Text("Clientes nuevos"),
                                        ft.Text("Avg %"),
                                    ],
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                                padding=10,
                            ),
                        ),
                        # Tasa dolar
                        ft.Card(
                            content=ft.Container(
                                content=ft.Column(
                                    controls=[
                                        ft.Icon(ft.Icons.ATTACH_MONEY),
                                        ft.Text("Tasa del dia"),
                                        ft.Row(
                                            controls=[
                                                ft.Text(
                                                    f"BCV: {usd_rate[:9]}",
                                                    weight=ft.FontWeight.BOLD,
                                                ),
                                            ],
                                            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                                        ),
                                    ],
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                                padding=10,
                            )
                        ),
                    ],
                    # expand=True,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def _on_card(self, e):
        is_hover = e.data == True

        contenedor = e.control

        contenedor.scale = 1.1 if is_hover else 1.0
        contenedor.update()


class IngresosData(ft.Container):
    def __init__(self):
        super().__init__(
            **container_style,
        )

        self.pagos = manejo_pagos.cargar_pagos()
        self.pagos_dolares = 0
        self.pagos_bolivares = 0

        self.left_axis = ft.ChartAxis(
            labels_size=40,
            show_labels=True,
        )
        # LABELS DE DIAS
        self.bottom_axis = ft.ChartAxis(
            labels=[  # Etiquetas fijas para los días
                ft.ChartAxisLabel(
                    value=0, label=ft.Container(ft.Text("Lun"), padding=5)
                ),
                ft.ChartAxisLabel(
                    value=1, label=ft.Container(ft.Text("Mar"), padding=5)
                ),
                ft.ChartAxisLabel(
                    value=2, label=ft.Container(ft.Text("Mié"), padding=5)
                ),
                ft.ChartAxisLabel(
                    value=3, label=ft.Container(ft.Text("Jue"), padding=5)
                ),
                ft.ChartAxisLabel(
                    value=4, label=ft.Container(ft.Text("Vie"), padding=5)
                ),
                ft.ChartAxisLabel(
                    value=5, label=ft.Container(ft.Text("Sáb"), padding=5)
                ),
                ft.ChartAxisLabel(
                    value=6, label=ft.Container(ft.Text("Dom"), padding=5)
                ),
            ],
            labels_size=40,
        )

        self.chart = ft.BarChart(
            bar_groups=[],
            left_axis=self.left_axis,
            bottom_axis=self.bottom_axis,
            horizontal_grid_lines=ft.ChartGridLines(
                color=ft.Colors.with_opacity(0.2, ft.Colors.ON_SURFACE), width=1
            ),
            tooltip_bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.SECONDARY),
            interactive=True,
            expand=True,
        )
        self.txt_total_semana = ft.Text(
            "Total Semana ($): ...", weight=ft.FontWeight.BOLD
        )

        self.content = ft.Column(
            controls=[
                ft.Text(
                    "Ingresos Diarios $ (Semana Actual)",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                ),
                self.chart,
                self.txt_total_semana,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
            spacing=10,
        )

    def cargar_grafica(self):
        barra_bs = ft.BarChartRod(
            from_y=0,
            width=25,  # Ancho de barra
            color="blue",  # Asignar color,
            border_radius=5,
        )
        barra_dolar = ft.BarChartRod(
            from_y=0,
            width=25,  # Ancho de barra
            color="green",  # Asignar color,
            border_radius=5,
        )
        nuevo_grupo = []
        for data in self.pagos:
            monto = data["monto"]
            if monto.startswith("Bs."):
                monto_limpio = monto.replace("Bs.", "").strip().replace(" ", "")
                print(monto_limpio)
                valor = Decimal(monto_limpio)
                self.pagos_bolivares += valor
                print(valor)
                barra_bs.to_y = float(self.pagos_bolivares)
                barra_bs.tooltip = f"Bs. {self.pagos_bolivares}"

            if monto.startswith("$"):
                monto_limpio = monto.replace("$", "").replace(" ", "")
                print(monto_limpio)
                valor_usd = Decimal(monto_limpio)
                self.pagos_dolares += valor_usd
                # print(valor)
                barra_dolar.to_y = float(self.pagos_dolares)
                barra_dolar.tooltip = f"USD{self.pagos_dolares}"

            if self.pagos_dolares > self.pagos_bolivares:
                self.chart.max_y = self.pagos_dolares + 20
            else:
                self.chart.max_y = self.pagos_bolivares + 20

        grupo = [ft.BarChartGroup(x=1, bar_rods=[barra_bs, barra_dolar])]
        self.txt_total_semana.value = (
            f"Total Semana $: {self.pagos_dolares} | Bs.:{self.pagos_bolivares}"
        )
        self.txt_total_semana.update()
        self.chart.bar_groups = grupo
        self.chart.update()
        self.pagos_bolivares = 0
        self.pagos_dolares = 0


class ServiciosData(ft.Container):
    def __init__(self):
        super().__init__(
            **container_style,
        )
        self.content = ft.Column(
            controls=[
                ft.Text(
                    "Top Servicios",
                    theme_style=ft.TextThemeStyle.TITLE_LARGE,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.DataTable(
                    columns=[
                        ft.DataColumn(label=ft.Text("#")),
                        ft.DataColumn(label=ft.Text("Descripcion")),
                        ft.DataColumn(label=ft.Text("Popularidad")),
                        ft.DataColumn(label=ft.Text("Sales")),
                    ],
                    rows=[
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text("#1")),
                                ft.DataCell(ft.Text("Cambio de croche")),
                                ft.DataCell(
                                    ft.ProgressBar(
                                        value=0.5,
                                        tooltip="jamon",
                                    ),
                                ),
                                ft.DataCell(
                                    ft.Container(
                                        content=ft.Text(
                                            "tango por",
                                        ),
                                        border=ft.border.all(1, "blue"),
                                        border_radius=10,
                                        padding=5,
                                        bgcolor=ft.Colors.RED_ACCENT,
                                    )
                                ),
                            ]
                        ),
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text("#2")),
                                ft.DataCell(ft.Text("Cambio de croche")),
                                ft.DataCell(
                                    ft.ProgressBar(
                                        value=0.5,
                                        tooltip="jamon",
                                    ),
                                ),
                                ft.DataCell(
                                    ft.Container(
                                        content=ft.Text(
                                            "tango por",
                                        ),
                                        border=ft.border.all(1, "blue"),
                                        border_radius=10,
                                        padding=5,
                                        bgcolor=ft.Colors.RED_ACCENT,
                                    )
                                ),
                            ]
                        ),
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text("#3")),
                                ft.DataCell(ft.Text("Cambio de croche")),
                                ft.DataCell(
                                    ft.ProgressBar(
                                        value=0.5,
                                        tooltip="jamon",
                                    ),
                                ),
                                ft.DataCell(
                                    ft.Container(
                                        content=ft.Text(
                                            "tango por",
                                        ),
                                        border=ft.border.all(1, "blue"),
                                        border_radius=10,
                                        padding=5,
                                        bgcolor=ft.Colors.RED_ACCENT,
                                    )
                                ),
                            ]
                        ),
                    ],
                ),
                # ft.Row(
                #     controls=[
                #         # ft.Text("Servicio 1"),
                #
                #     ]
                # ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        )


class OrdenesData(ft.Container):
    def __init__(self):
        super().__init__(
            **container_style,
        )

        self.tabla = ft.DataTable(
            columns=[
                ft.DataColumn(label=ft.Text("Servicio")),
                ft.DataColumn(label=ft.Text("Fecha de entrega")),
                ft.DataColumn(label=ft.Text("Estado")),
            ],
            rows=[],
            # column_spacing=20,
            # heading_row_height=40,
            # data_row_max_height=50,
            border=ft.border.all(1, ft.Colors.with_opacity(0.1, ft.Colors.ON_SURFACE)),
            border_radius=ft.border_radius.all(6),
        )
        self.content = ft.Column(
            controls=[
                ft.Text(
                    "Órdenes Recientes / Pendientes",  # Título más descriptivo
                    theme_style=ft.TextThemeStyle.TITLE_MEDIUM,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Row(
                    controls=[
                        ft.ElevatedButton(
                            "Añadir orden",
                        ),
                        ft.ElevatedButton("Limpiar"),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                self.tabla,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def actualizar_tabla(self, descripcion, fecha_entrega, estado):
        row = ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(descripcion)),
                ft.DataCell(ft.Text(fecha_entrega)),
                ft.DataCell(ft.Text(estado)),
            ]
        )

        self.tabla.rows.insert(0, row)

        self.tabla.update()


# Instancias de clases
container_cliente = TotalData()
container_pago = IngresosData()
container_servicios = ServiciosData()
container_ordenes_home = OrdenesData()


def carga_tabla_ordenes():
    ordenes = manejo_ordenes.cargar_ordenes()
    ordenes.reverse()
    for orden in ordenes:
        row = ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(orden["servicio"])),
                ft.DataCell(ft.Text(orden["fecha"])),
                ft.DataCell(ft.Text("alasdnmoa")),
            ]
        )

        container_ordenes_home.tabla.rows.append(row)

    container_ordenes_home.tabla.update()


def actualizar_dashboard(e):
    try:
        lista_clientes = manejo_cliente.cargar_clientes()
        total_clientes = len(lista_clientes) if lista_clientes else 0
        container_cliente.txt_total_clientes.value = str(total_clientes)
        if container_cliente.page:
            container_cliente.txt_total_clientes.update()
        print(f"Clientes totales: {total_clientes}")
    except Exception as ex:
        print(f"Error al actualizar clientes totales {e}")


# region VISTA
class HomeUiState(ft.Container):
    def __init__(self):
        super().__init__(expand=True, padding=ft.padding.only(top=5))
        self.content = ft.Column(
            controls=[
                ft.ResponsiveRow(
                    controls=[
                        ft.Container(content=container_cliente),
                    ]
                ),
                ft.ResponsiveRow(
                    controls=[
                        # ft.Container(
                        #     content=container_pago,
                        #     col=6,
                        # ),
                        ft.Container(content=container_servicios, col=6),
                        ft.Container(content=container_ordenes_home, col=6),
                    ]
                ),
            ],
            expand=True,
        )


home = HomeUiState()
