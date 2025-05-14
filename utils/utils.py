import flet as ft
from typing import Optional

from logica.manejo_cliente import ManejoCliente


class DialogHandler:
    def __init__(self):
        def close_dialog(self, e):
            e.page.overlay[-1].open = False
            e.page.update()
            e.page.overlay.pop()

    @staticmethod
    def crear_dialogo_confirmacion(page, titulo: str, mensaje: str, on_confirm):
        def cerrar_dialogo(e):
            e.page.overlay[-1].open = False
            e.page.update()
            e.page.overlay.pop()

        dialogo = ft.AlertDialog(
            modal=True,
            title=ft.Text(titulo),
            content=ft.Text(mensaje),
            actions=[
                ft.TextButton("Confirmar", on_click=on_confirm),
                ft.TextButton("Cancelar", on_click=cerrar_dialogo),
            ],
        )
        page.overlay.append(dialogo)
        dialogo.open = True
        page.update()

    @staticmethod
    def crear_dialogo_edicion(
        page,
        cliente_data: dict,
        manejo_cliente: ManejoCliente,
        on_edit: Optional[callable] = None,
    ):
        def cerrar_dialogo(e):
            if page.overlay and isinstance(page.overlay[-1], ft.AlertDialog):
                page.overlay[-1].open = False  # Marcar para cerrar
                page.update()  # Actualizar la UI para ocultarlo
                # page.overlay.pop()  # Eliminar del stack (después de actualizar)

        # Creamos los campos de texto con los datos del cliente
        txt_nombre = crear_campo_texto(
            label="Nombre y Apellido", value=cliente_data.get("Nombre", "")
        )
        txt_telefono = crear_campo_texto(
            label="Telefono", value=cliente_data.get("Telefono", "")
        )
        txt_direccion = crear_campo_texto(
            label="Dirección", value=cliente_data.get("Direccion", "")
        )

        def confirmacion(e):
            datos_actualizados = {
                "id": cliente_data.get("Id"),
                "nombre": txt_nombre.value.strip(),
                "telefono": txt_telefono.value.strip(),
                "direccion": txt_direccion.value,
            }
            resultado_edicion = manejo_cliente.editar_cliente(
                datos_actualizados["id"],
                datos_actualizados["nombre"],
                datos_actualizados["telefono"],
                datos_actualizados["direccion"],
            )
            if isinstance(resultado_edicion, dict) and "errors" in resultado_edicion:
                errores_api = resultado_edicion["errors"]
                if "telefono" in errores_api:
                    txt_telefono.error_text = "Este numero ya esta registrado"
                    txt_telefono.update()
                return
            else:
                cerrar_dialogo(e)
                page.open(ft.SnackBar(ft.Text("Cliente editado exitosamente")))
                if on_edit:
                    on_edit()

        dialogo = ft.AlertDialog(
            modal=True,
            title=ft.Text("Editar cliente"),
            content=ft.Column(
                controls=[txt_nombre, txt_telefono, txt_direccion], spacing=20
            ),
            actions=[
                ft.TextButton("Confirmar", on_click=confirmacion),
                ft.TextButton("Cancelar", on_click=cerrar_dialogo),
            ],
        )
        page.overlay.append(dialogo)
        dialogo.open = True
        page.update()

    @staticmethod
    def crear_dialogo_edicion_servicio(page, servicio_data: dict, on_edit):
        def cerrar_dialogo(e):
            e.page.overlay[-1].open = False
            e.page.update()
            e.page.overlay.pop()

        # Creamos los campos de texto con los datos del cliente
        txt_descripcion = crear_campo_texto(
            label="Descripcion", value=servicio_data["Descripcion"]
        )
        txt_precio = crear_campo_texto(label="Precio", value=servicio_data["Precio"])

        def confirmacion(e):
            on_edit(
                {
                    "id": servicio_data["Id"],
                    "descripcion": txt_descripcion.value,
                    "precio": txt_precio.value,
                }
            )

            cerrar_dialogo(e)

        dialogo = ft.AlertDialog(
            modal=True,
            title=ft.Text("Editar servicio"),
            content=ft.Column(controls=[txt_descripcion, txt_precio], spacing=20),
            actions=[
                ft.TextButton("Confirmar", on_click=confirmacion),
                ft.TextButton("Cancelar", on_click=cerrar_dialogo),
            ],
        )
        page.overlay.append(dialogo)
        dialogo.open = True
        page.update()


def crear_campo_texto(label, hint_text: Optional[str] = None, value: str = None):
    "Crea un campo de texto estilizado"
    return ft.TextField(
        label=label,
        hint_text=hint_text,
        value=value,
        width=300,
        border_color="#2196f3",
        border=ft.InputBorder.UNDERLINE,
    )


def crear_boton(
    text,
    icon: Optional[str] = None,
    on_click: Optional[vars] = None,
    color: Optional[str] = None,
):
    "Creamos un boton estilizado"
    return ft.ElevatedButton(
        text=text,
        icon=icon,
        # width=150,
        style=ft.ButtonStyle(color=color),
        on_click=on_click,
        disabled=True,
        width=150,
    )


def manejar_seleccion(e):
    # Obtener la fila seleccionada
    fila_seleccionada = e.control  # Esto devuelve la instancia de DataRow seleccionada

    # Alternar el estado de selección
    fila_seleccionada.selected = not fila_seleccionada.selected
    fila_seleccionada.update()  # Actualizar la fila en la interfaz

    if fila_seleccionada.selected:  # Verificar si la fila está seleccionada
        # Acceder al contenido de la primera celda (ID)
        id_seleccionado = fila_seleccionada.cells[0].content.value
        print(f"El ID es: {id_seleccionado}")
    else:
        print("Fila deseleccionada")
