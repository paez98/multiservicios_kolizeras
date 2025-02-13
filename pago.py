import flet as ft
from datetime import datetime

# ===============================================
#     ELEMENTOS DE LA INTERFAZ DE PAGOS
# ===============================================

# Dropdowns y campos de entrada
dd_cliente = ft.Dropdown(
    label="Cliente",
    width=300,
    options=[
        ft.dropdown.Option("Juan Pérez"),
        ft.dropdown.Option("María García"),
        ft.dropdown.Option("Carlos Martínez")
    ],
    border_color="#9C27B0"
)

dd_servicio = ft.Dropdown(
    label="Servicio",
    width=300,
    options=[
        ft.dropdown.Option("Cambio de aceite"),
        ft.dropdown.Option("Alineación"),
        ft.dropdown.Option("Frenos")
    ],
    border_color="#9C27B0"
)

txt_monto = ft.TextField(
    label="Monto",
    width=200,
    border_color="#9C27B0",
    prefix_text="$",
    hint_text="Ej: 150.000"
)

# Botón de registro de pago
btn_registrar_pago = ft.ElevatedButton(
    text="Registrar Pago",
    icon=ft.icons.PAYMENT,
    style=ft.ButtonStyle(
        bgcolor="#9C27B0",
        color="white"
    ),
    width=200
)

# Tabla de pagos
tabla_pagos = ft.DataTable(
    columns=[
        ft.DataColumn(ft.Text("Cliente")),
        ft.DataColumn(ft.Text("Servicio")),
        ft.DataColumn(ft.Text("Monto")),
        ft.DataColumn(ft.Text("Fecha")),
        ft.DataColumn(ft.Text("Estado")),
    ],
    rows=[
        ft.DataRow(
            cells=[
                ft.DataCell(ft.Text("Juan Pérez")),
                ft.DataCell(ft.Text("Alineación")),
                ft.DataCell(ft.Text("$75.000")),
                ft.DataCell(ft.Text("2023-08-15")),
                ft.DataCell(ft.Text("Pagado", color=ft.colors.GREEN)),
            ]
        )
    ],
    expand=True
)

# Contenedor principal de pagos
pago_container = ft.Container(
    content=ft.Column(
        controls=[
            ft.Text("Registro de Pagos", size=25, color="#9C27B0"),
            ft.Row(
                controls=[
                    dd_cliente,
                    dd_servicio,
                    txt_monto,
                    btn_registrar_pago
                ],
                spacing=20,
                alignment=ft.MainAxisAlignment.CENTER
            ),
            ft.Divider(height=20),
            ft.Container(
                content=tabla_pagos,
                border=ft.border.all(1, "#E1BEE7"),
                border_radius=10,
                padding=10,
                expand=True,
                alignment=ft.alignment.top_center
            )
        ],
        spacing=20,
        expand=True
    ),
    padding=20,
    expand=True
)
