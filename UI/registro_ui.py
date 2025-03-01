import flet as ft
from utils.utils import crear_campo_texto
from logica.crear_cliente import guardar_cliente
# from ui.cliente_ui import cargar_clientes_en_tabla


def limpiar_campos(txt_nombre, txt_contacto, txt_direccion):
    """Limpia los campos del diálogo."""
    txt_nombre.value = ""
    txt_contacto.value = ""
    txt_direccion.value = ""
    txt_nombre.error_text = ""
    txt_contacto.error_text = ""
    txt_nombre.update()
    txt_contacto.update()
    txt_direccion.update()


def validar_campos(nombre, contacto):
    """Valida los campos obligatorios."""
    errores = {}
    if not nombre:
        errores["nombre"] = "Campo obligatorio"
    if not contacto:
        errores["contacto"] = "Campo obligatorio"
    return errores


def guardar_cliente_desde_dialogo(e, txt_nombre, txt_contacto, txt_direccion):
    """Guarda un cliente desde el diálogo modal."""
    errores = validar_campos(txt_nombre.value.strip(), txt_contacto.value.strip())
    if errores:
        txt_nombre.error_text = errores.get("nombre", "")
        txt_contacto.error_text = errores.get("contacto", "")
        txt_nombre.update()
        txt_contacto.update()
        return

    # Guardar el cliente
    guardar_cliente(
        txt_nombre.value.strip(),
        txt_contacto.value.strip(),
        txt_direccion.value.strip(),
    )

    # Limpiar los campos
    limpiar_campos(txt_nombre, txt_contacto, txt_direccion)

    # Cerrar el diálogo
    e.page.overlay[-1].open = False  # Cierra el último diálogo en el overlay
    e.page.update()
    e.page.overlay.pop()
    # cargar_clientes_en_tabla()


def crear_dialogo_agregar_cliente(e):
    """Crea y abre un diálogo modal para añadir un cliente."""

    def close_dlg(e):
        """Cierra el dialogo modal"""
        # """Cierra el diálogo modal."""
        e.page.overlay[-1].open = False
        e.page.update()
        e.page.overlay.pop()  # Elimina el diálogo del overlay

    # Crear campos de texto
    txt_nombre = crear_campo_texto("Nombre y Apellido", "Ej: Alissa")
    txt_contacto = crear_campo_texto("Telefono", "Ej: +123456789")
    txt_direccion = crear_campo_texto("Direccion", "Ej: Direccion 1234 calle 12")

    # Crear el diálogo modal
    dlg_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Registrar Cliente", text_align=ft.TextAlign.CENTER),
        content=ft.Column(
            controls=[
                txt_nombre,
                txt_contacto,
                txt_direccion,
            ],
            spacing=30,
            width=400,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            height=350,
        ),
        actions=[
            ft.TextButton(
                "Guardar",
                style=ft.ButtonStyle(bgcolor="green", color="white"),
                on_click=lambda e: guardar_cliente_desde_dialogo(
                    e,
                    txt_nombre,
                    txt_contacto,
                    txt_direccion,
                ),
            ),
            ft.TextButton(
                "Cancelar",
                style=ft.ButtonStyle(bgcolor="red", color="white"),
                on_click=close_dlg,
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.SPACE_EVENLY,
    )

    # Abrir el diálogo
    e.control.page.overlay.append(dlg_modal)
    dlg_modal.open = True
    e.control.page.update()
