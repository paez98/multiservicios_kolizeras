import flet as ft
from utils.utils import crear_campo_texto
from logica.manejo_cliente import ManejoCliente
from logica.manejo_servicio import ManejoServicio
from logica.logica_pago import LogicaPago

manejo_cliente = ManejoCliente()


# region CLIENTES
def validar_campos(nombre: str, contacto: str):
    """Valida los campos obligatorios."""
    errores = {}
    if not nombre.strip() or len(nombre) < 5:
        errores["nombre"] = "Nombre invalido"
    if not contacto.strip().isdigit() or len(contacto.strip()) < 8:
        errores["contacto"] = "telefono invalido"
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
    manejo_cliente.guardar_cliente(
        txt_nombre.value.strip(),
        txt_contacto.value.strip(),
        txt_direccion.value.strip(),
    )

    # Limpiar los campos
    # limpiar_campos(txt_nombre, txt_contacto, txt_direccion)

    # Cerrar el diálogo
    e.page.overlay[-1].open = False  # Cierra el último diálogo en el overlay
    e.page.update()
    e.page.overlay.pop()


def crear_dialogo_agregar_cliente(e):
    """Crea y abre un diálogo modal para añadir un cliente."""

    def close_dlg(e):
        """Cierra el dialogo modal"""
        # """Cierra el diálogo modal."""
        e.page.overlay[-1].open = False
        e.page.update()
        e.page.overlay.pop()  # Elimina el diálogo del overlay

    # Crear campos de texto
    txt_nombre = crear_campo_texto(label="Nombre y Apellido", hint_text="Alissa Paez")
    txt_contacto = crear_campo_texto(label="Contacto", hint_text="04123550450")
    txt_direccion = crear_campo_texto(
        label="Direccion", hint_text="Urb. Parque Valencia"
    )

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


# region SERVICIOS
manejo_servicio = ManejoServicio()


def validar_campos_servicio(descripcion: str, precio: str):
    """Valida los campos obligatorios."""
    errores = {}
    if not descripcion.strip() or len(descripcion) < 5:
        errores["descripcion"] = "Descripcion invalida"
    if not precio.strip().isdigit():
        errores["precio"] = "Precio invalido"
    return errores


def guardar_desde_dialogo(e, txt_descripcion, txt_precio):
    errores = validar_campos_servicio(
        txt_descripcion.value.strip(), txt_precio.value.strip()
    )
    if errores:
        txt_descripcion.error_text = errores.get("descripcion", "")
        txt_precio.error_text = errores.get("precio", "")
        txt_descripcion.update()
        txt_precio.update()
        return
    monto_completo = f"{txt_precio.prefix_text + txt_precio.value}"
    manejo_servicio.guardar_servicio(
        txt_descripcion.value.strip(), monto_completo.strip()
    )
    e.page.overlay[-1].open = False  # Cierra el último diálogo en el overlay
    e.page.update()
    e.page.overlay.pop()


def crear_dialogo_agregar_servicio(e):
    def close_dlg(e):
        """Cierra el dialogo modal"""
        # """Cierra el diálogo modal."""
        e.page.overlay[-1].open = False
        e.page.update()
        e.page.overlay.pop()  # Elimina el diálogo del overlay

    txt_descripcion = crear_campo_texto("Descripción", "Cambio de croche")
    txt_precio = crear_campo_texto("Precio", "150")
    txt_precio.prefix_text = "$"

    # Crear dialogo modal
    dlg_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Registrar Servicio", text_align=ft.TextAlign.CENTER),
        content=ft.Column(
            controls=[txt_descripcion, txt_precio],
            spacing=30,
            width=400,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            height=350,
        ),
        actions=[
            ft.TextButton(
                "Guardar",
                style=ft.ButtonStyle(bgcolor="green", color="white"),
                on_click=lambda e: guardar_desde_dialogo(
                    e, txt_descripcion, txt_precio
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


# region PAGOS
manejo_pago = LogicaPago()


def guardar_pago(e, nombre, servicio, monto, fecha):
    """Guarda un pago en la base de datos"""
    try:
        response = manejo_pago.guardar_pago(nombre, servicio, monto, fecha)
        print(f"Pago guardado exitosamente {response}")
        return response.data
    except Exception as e:
        print(f"Error al guardar el pago: {e}")
        return None
