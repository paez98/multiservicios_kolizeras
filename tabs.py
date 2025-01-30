import flet as ft
from taller_app import lista_clientezx
from servicios import lista_servicios


def main(page: ft.Page):

    t = ft.Tabs(
        selected_index=1,
        animation_duration=300,
        tabs=[
            ft.Tab(
                text="Clientes",
                icon=ft.Icons.PEOPLE_ALT,
                content=ft.Container(
                    lista_clientezx
                ),
            ),
            ft.Tab(
                text='Servicios',
                icon=ft.Icon(ft.Icons.DESIGN_SERVICES),
                content=ft.Container(
                    lista_servicios
                )
            ),
            ft.Tab(
                text="Tab 3",
                icon=ft.Icons.SETTINGS,
                content=ft.Text("This is Tab 3"),
            ),
        ],
        expand=1,
    )

    page.add(t)

    ft.app(main)
