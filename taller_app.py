import flet as ft


def main(page: ft.Page):
    # Configuración de la ventana
    page.title = "Taller Mecánico App"
    page.window_width = 1000
    page.window_height = 600
    page.window_resizable = True  # Permite redimensionar

    # ========================================
    # ELEMENTOS DE LA INTERFAZ (Solo gráficos)
    # ========================================

    # --- Campos del formulario ---
    txt_nombre = ft.TextField(
        label="Nombre del cliente",
        width=300,
        border_color="#2196F3",  # Color del borde
        hint_text="Ej: Juan Pérez"
    )

    txt_contacto = ft.TextField(
        label="Contacto",
        width=300,
        border_color="#2196F3",
        hint_text="Ej: +56912345678"
    )

    btn_guardar = ft.ElevatedButton(
        text="Guardar Cliente",
        icon=ft.Icons.SAVE_OUTLINED,
        width=100,
        height=50,
        style=ft.ButtonStyle(
            bgcolor="#2196F3",
            color="white"
        )
    )

    # --- Sección del formulario (Izquierda) ---
    seccion_formulario = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Registrar Cliente", size=25, color="#2196F3"),
                txt_nombre,
                txt_contacto,
                btn_guardar
            ],
            spacing=20  # Espacio entre elementos
        ),
        padding=30,
        border=ft.border.all(2, "#BBDEFB"),
        border_radius=10,
        margin=20
    )

    # --- Lista de clientes (Derecha) ---
    titulo_clientes = ft.Text("Clientes Registrados", size=20, color="#2196F3")

    lista_clientes = ft.Column(
        spacing=10,
        scroll=ft.ScrollMode.ALWAYS,  # Permite desplazamiento
        height=400  # Altura fija
    )

    # Botón de actualizar manual
    btn_actualizar = ft.ElevatedButton(
        "Actualizar Lista",
        icon=ft.Icons.REFRESH
    )

    # Contenedor de la lista
    seccion_lista = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row([titulo_clientes, btn_actualizar],
                       alignment="spaceBetween"),
                ft.Divider(),
                lista_clientes
            ],
            spacing=20
        ),
        padding=30,
        border=ft.border.all(2, "#BBDEFB"),
        border_radius=10,
        margin=20,
        expand=True  # Ocupa todo el espacio disponible
    )

    # ========================================
    # DISEÑO FINAL DE LA PÁGINA
    # ========================================
    page.add(
        ft.Row(
            controls=[seccion_formulario, seccion_lista],
            spacing=0.5,
            expand=True
        )
    )


ft.app(target=main)
