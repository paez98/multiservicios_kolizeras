import flet as ft


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
                        ft.ElevatedButton("Añadir orden"),
                        ft.ElevatedButton("Limpiar"),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                self.tabla,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )


container_ordenes = OrdenesData()
