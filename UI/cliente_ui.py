import flet as ft

# ===============================================
#     ELEMENTOS DE LA INTERFAZ (Solo gráficos)
# ===============================================
txt_nombre = ft.TextField(
    label="Nombre del cliente",
    width=300,
    border_color="#2196F3",
    hint_text="Ej: Alissa")

txt_contacto = ft.TextField(
    label="Contacto",
    width=300,
    border_color="#2196F3",
    hint_text="Ej: +56912345678"
)


btn_eliminar = ft.ElevatedButton(
    text='Eliminar',
    icon=ft.Icons.DELETE_FOREVER,
    width=200,
    height=50,

    style=ft.ButtonStyle(
        bgcolor="red",
        color="white",
    ),
)

btn_guardar = ft.ElevatedButton(
    text='Guardar',
    icon=ft.Icons.SAVE_SHARP,
    width=200,
    height=50,
    style=ft.ButtonStyle(
        bgcolor="#2196F3",
        color="white",
    ),
)

btn_editar = ft.ElevatedButton(
    text='Editar',
    icon=ft.Icons.EDIT_SQUARE,
    width=200,
    height=50,
    style=ft.ButtonStyle(
        bgcolor="yellow",
        color="dark-yellow",
    ),
)
lista_clientes = ft.DataTable(
    columns=[
        ft.DataColumn(ft.Text("First name")),
        ft.DataColumn(ft.Text("Last name")),
        ft.DataColumn(ft.Text("Age"), numeric=True),
    ],
    rows=[
        ft.DataRow(
            cells=[
                ft.DataCell(ft.Text("John")),
                ft.DataCell(ft.Text("Smith")),
                ft.DataCell(ft.Text("43")),
            ],
        ),
        ft.DataRow(
            cells=[
                ft.DataCell(ft.Text("Jack")),
                ft.DataCell(ft.Text("Brown")),
                ft.DataCell(ft.Text("19")),
            ],
        ),
        ft.DataRow(
            cells=[
                ft.DataCell(ft.Text("Alice")),
                ft.DataCell(ft.Text("Wong")),
                ft.DataCell(ft.Text("25")),
            ],
        ),
    ],

    expand=True
)


vista_clientes = ft.Container(
    content=ft.Row(
        controls=[
            # Campos del formularioS
            ft.Column(
                controls=[
                    ft.Text('Registrar cliente', size=30, weight=200),
                    txt_nombre,
                    txt_contacto,
                    btn_guardar,
                    btn_eliminar,
                    btn_editar
                ],
                # expand=True
            ),
            ft.Column(

                [lista_clientes],

                #   alignment=ft.CrossAxisAlignment.START
            )
            # Lista de clientes
        ],
        spacing=40,
        expand=True
        # alignment=ft.CrossAxisAlignment.START,

    ),
    border=ft.border.all(2, "#BBDEFB"),
    expand=True
    # border_radius=10,
)
