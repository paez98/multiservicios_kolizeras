import flet as ft


def RegistroUI(page: ft.Page):
    """
    Interfaz gráfica para el formulario de registro.
    :param page: Instancia de la página principal (usada para abrir/cerrar diálogos).
    :return: Diálogo modal con el formulario de registro.
    """
    # Campos del formulario
    txt_nombre = ft.TextField(
        label="Nombre del cliente",
        width=300,
        border_color="#2196F3",
        hint_text="Ej: Alissa",
        text_style=ft.TextStyle(size=14),
        border_radius=8,
        content_padding=10
    )
    txt_contacto = ft.TextField(
        label="Contacto",
        width=300,
        border_color="#2196F3",
        hint_text="Ej: +56912345678",
        text_style=ft.TextStyle(size=14),
        border_radius=8,
        content_padding=10
    )
    txt_direccion = ft.TextField(
        label="Dirección",
        width=300,
        border_color="#2196F3",
        hint_text="Ej: Calle Principal #123",
        text_style=ft.TextStyle(size=14),
        border_radius=8,
        content_padding=10
    )

    # Diálogo modal para el formulario de registro
    dlg_registro = ft.AlertDialog(
        title=ft.Text("Registrar Cliente", size=20,
                      weight="bold", color="#2196F3"),
        content=ft.Column(
            controls=[
                txt_nombre,
                txt_contacto,
                txt_direccion,
                ft.ElevatedButton(
                    text="Guardar",
                    icon=ft.icons.SAVE_SHARP,
                    width=200,
                    height=50,
                    style=ft.ButtonStyle(
                        bgcolor="#2196F3",
                        color="white"
                    ),
                    on_click=lambda e: guardar_cliente_nuevo(e, dlg_registro)
                )
            ],
            spacing=15,
            horizontal_alignment="center"
        ),
        actions=[
            ft.TextButton(
                "Cancelar",
                on_click=lambda e: close_dialog(dlg_registro),
                style=ft.ButtonStyle(color="#2196F3")
            )
        ],
        actions_alignment="end",
        shape=ft.RoundedRectangleBorder(radius=10),
        bgcolor="#FAFAFA"
    )

    def open_registro_dialog(e):
        """Abre el diálogo de registro."""
        page.dialog = dlg_registro
        dlg_registro.open = True
        page.update()

    def close_dialog(dialog):
        """Cierra el diálogo."""
        dialog.open = False
        page.update()

    def guardar_cliente_nuevo(e, dialog):
        """Guarda un nuevo cliente desde el diálogo."""
        nombre = txt_nombre.value.strip()
        contacto = txt_contacto.value.strip()
        direccion = txt_direccion.value.strip()

        if not nombre or not contacto:
            txt_nombre.error_text = "Campo obligatorio" if not nombre else ""
            txt_contacto.error_text = "Campo obligatorio" if not contacto else ""
            page.update()
            return

        # Aquí puedes llamar a la función de lógica para guardar el cliente
        print(f"Cliente guardado: {nombre}, {contacto}, {direccion}")

        # Limpia los campos después de guardar
        txt_nombre.value = ""
        txt_contacto.value = ""
        txt_direccion.value = ""
        txt_nombre.error_text = ""
        txt_contacto.error_text = ""

        # Cierra el diálogo
        close_dialog(dialog)

    # Retorna la función para abrir el diálogo
    return open_registro_dialog
