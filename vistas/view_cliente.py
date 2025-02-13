import flet as ft
from logica.crear_cliente import guardar_cliente
from logica.eliminar_cliente import eliminar_cliente
from logica.editar_cliente import editar_cliente
from logica.cargar_cliente import cargar_clientes
# from ui.cliente_ui import lista_clientes

view_cliente = ft.Container(
    content=[
        ft.Column(
            [
                ft.Text('Clientes Registrados', size=25, weight='bold'),
                ft.ElevatedButton(
                    text='Añadir cliente',
                    icon=ft.Icons.PERSON_ADD_ALT,
                    width=200,
                    height=50,
                    style=ft.ButtonStyle(
                        bgcolor="#2196F3",
                        color="white"
                    )
                )
            ]
        )



        # lista_clientes

    ]
)
