import flet as ft

lista_servicios = ft.DataTable(
    columns=[
        ft.DataColumn(ft.Text('Nombre')),
        ft.DataColumn(ft.Text('Vehiculo')),
        ft.DataColumn(ft.Text('Costo')),
    ],
    rows=[
        ft.DataRow(
            cells=[
                ft.DataCell(ft.Text('Cambio de croche')),
                ft.DataCell(ft.Text('Spark')),
                ft.DataCell(ft.Text('100$'))
            ]
        )
    ]
)
