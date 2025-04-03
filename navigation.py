import flet as ft

nav = ft.NavigationBar(
    destinations=[
        ft.NavigationBarDestination(icon=ft.Icons.EXPLORE, label="Home"),
        ft.NavigationBarDestination(icon=ft.Icons.COMMUTE, label="Clientes"),
        ft.NavigationBarDestination(
            icon=ft.Icons.BOOKMARK_BORDER,
            selected_icon=ft.Icons.BOOKMARK,
            label="Servicios",
        ),
        ft.NavigationBarDestination(
            label="Pago",
        ),
        ft.NavigationBarDestination(
            label="Pago",
        ),
    ],
)

rail = ft.NavigationRail(
    selected_index=0,
    # label_type=ft.NavigationRailLabelType.SELECTED,
    # extended=True,
    group_alignment=-1,
    destinations=[
        ft.NavigationRailDestination(
            icon=ft.Icons.FAVORITE_BORDER,
            selected_icon=ft.Icons.FAVORITE,
            label="First",
        ),
        ft.NavigationRailDestination(
            icon=ft.Icon(ft.Icons.BOOKMARK_BORDER),
            selected_icon=ft.Icon(ft.Icons.BOOKMARK),
            label="Second",
        ),
        ft.NavigationRailDestination(
            icon=ft.Icons.SETTINGS_OUTLINED,
            selected_icon=ft.Icon(ft.Icons.SETTINGS),
            label_content=ft.Text("Settings"),
        ),
    ],
    on_change=lambda e: print("Selected destination:", e.control.selected_index),
)
