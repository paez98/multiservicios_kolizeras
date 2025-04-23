import flet as ft
from tasa import usd_rate
from style import Colores
from logica.manejo_cliente import ManejoCliente

manejo_cliente = ManejoCliente()

container_style = {
    "border_radius": 10,
    "padding": 5,
}


class TotalData(ft.Container):
    def __init__(self):
        super().__init__(
            **container_style, border=ft.border.all(1, Colores.COLOR_BORDE.value)
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

    def actualizar_clientes_totales(self, valor: int):
        self.txt_total_clientes.value = str(valor)


"CREAR LA FUNCION PARA QUE SE ACTUALICE EL DASHBOARD Y EVITAR LA CARGA INICIAL DE LOS DATOS"


class IngresosData(ft.Container):
    def __init__(self):
        super().__init__(border=ft.border.all(1, "blue"), padding=10)
        self.chart = ft.BarChart(
            bar_groups=[
                # Barra lunes
                ft.BarChartGroup(
                    x=0,
                    bar_rods=[
                        ft.BarChartRod(
                            from_y=0,
                            to_y=40,
                            # width=,
                            color=ft.Colors.AMBER,
                            tooltip="Apple",
                            border_radius=15,
                        ),
                    ],
                ),
                # Barra martes
                ft.BarChartGroup(
                    x=1,
                    bar_rods=[
                        ft.BarChartRod(
                            from_y=0,
                            to_y=100,
                            # width=,
                            color=ft.Colors.RED,
                            tooltip="Blueberry",
                            border_radius=15,
                        ),
                    ],
                ),
                # Barra miercoles
                ft.BarChartGroup(
                    x=2,
                    bar_rods=[
                        ft.BarChartRod(
                            from_y=0,
                            to_y=30,
                            # width=,
                            color=ft.Colors.RED,
                            tooltip="Cherry",
                            border_radius=15,
                        ),
                    ],
                ),
                # Barra jueves
                ft.BarChartGroup(
                    x=3,
                    bar_rods=[
                        ft.BarChartRod(
                            from_y=0,
                            to_y=60,
                            # width=,
                            color=ft.Colors.ORANGE,
                            tooltip="Orange",
                            border_radius=15,
                        ),
                    ],
                ),
                # Barra viernes
                ft.BarChartGroup(
                    x=4,
                    bar_rods=[
                        ft.BarChartRod(
                            from_y=0,
                            to_y=60.5,
                            # width=,
                            color=ft.Colors.AMBER,
                            tooltip="manzana",
                            border_radius=15,
                        ),
                    ],
                ),
                # Barra sabado
                ft.BarChartGroup(
                    x=5,
                    bar_rods=[
                        ft.BarChartRod(
                            from_y=0,
                            to_y=60.5,
                            # width=,
                            color=ft.Colors.AMBER,
                            tooltip="manzana",
                            border_radius=15,
                        ),
                    ],
                ),
            ],
            left_axis=ft.ChartAxis(
                labels_size=40,
                show_labels=True,
            ),
            bottom_axis=ft.ChartAxis(
                labels=[
                    ft.ChartAxisLabel(
                        value=0, label=ft.Container(ft.Text("Lunes"), padding=10)
                    ),
                    ft.ChartAxisLabel(
                        value=1, label=ft.Container(ft.Text("Martes"), padding=10)
                    ),
                    ft.ChartAxisLabel(
                        value=2, label=ft.Container(ft.Text("Miercoles"), padding=10)
                    ),
                    ft.ChartAxisLabel(
                        value=3, label=ft.Container(ft.Text("Jueves"), padding=10)
                    ),
                    ft.ChartAxisLabel(
                        value=4, label=ft.Container(ft.Text("Viernes"), padding=10)
                    ),
                    ft.ChartAxisLabel(
                        value=5, label=ft.Container(ft.Text("Sabado "), padding=10)
                    ),
                ],
                labels_size=40,
            ),
            horizontal_grid_lines=ft.ChartGridLines(color=ft.Colors.GREY_300, width=1),
            tooltip_bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.GREY_300),
            interactive=True,
            expand=True,
            border=ft.border.all(1, "orange"),
        )

        self.content = ft.Column(
            controls=[ft.Text("Ingresos Semanales"), self.chart, ft.Text("Total: ")],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )


class PagosData(ft.Container):
    def __init__(self):
        super().__init__()
        self.content = ft.Row(
            controls=[
                ft.Container(content=ft.Column([ft.Text("Ingresos del mes")])),
                ft.Container(content=ft.Column([ft.Text("Pagos del mes")])),
            ]
        )


class ServiciosData(ft.Container):
    def __init__(self):
        super().__init__(
            border=ft.border.all(1, "yellow"),
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
        super().__init__(border=ft.border.all(1, "red"))

        self.tabla = ft.DataTable(
            columns=[
                ft.DataColumn(label=ft.Text("Nombre")),
                ft.DataColumn(label=ft.Text("Mecanico")),
                ft.DataColumn(label=ft.Text("Fecha de entrega")),
                ft.DataColumn(label=ft.Text("Estado")),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Motor de spark")),
                        ft.DataCell(ft.Text("Axel Paez")),
                        ft.DataCell(ft.Text("May 25,2025")),
                        ft.DataCell(
                            ft.Text("Completado", color=ft.Colors.GREEN_ACCENT_400)
                        ),
                    ]
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Cambio de croche")),
                        ft.DataCell(ft.Text("Adrian")),
                        ft.DataCell(ft.Text("Mar 13,2025")),
                        ft.DataCell(
                            ft.Text("En proceso", color=ft.Colors.DEEP_ORANGE_ACCENT)
                        ),
                    ]
                ),
            ],
        )
        self.content = ft.Column(
            controls=[
                ft.Text(
                    "Ordenes de Trabajo", theme_style=ft.TextThemeStyle.TITLE_LARGE
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


# Instancias de clases
container_cliente = TotalData()
container_pago = IngresosData()
container_servicios = ServiciosData()


def actualizar_dashboard(e=None):
    lista_clientes = manejo_cliente.cargar_clientes()
    total_clientes = len(lista_clientes) if lista_clientes else 0

    container_cliente.actualizar_clientes_totales(total_clientes)

    if container_cliente.page:
        container_cliente.txt_total_clientes.update()
    print(f"Clientes totales: {total_clientes}")


class HomeUiState(ft.Container):
    def __init__(self):
        super().__init__(**container_style, expand=True)
        self.content = ft.Column(
            controls=[
                ft.ResponsiveRow(
                    controls=[
                        ft.Container(content=container_cliente),
                    ]
                ),
                ft.ResponsiveRow(
                    controls=[
                        ft.Container(
                            content=container_pago,
                            col=6,
                            # offset=ft.transform.Offset(0, -0.31),
                        ),
                        ft.Container(content=container_servicios, col=6),
                        # ft.Container(content=container_ordenes, col=6),
                    ]
                ),
            ],
            expand=True,
        )


home = HomeUiState()
