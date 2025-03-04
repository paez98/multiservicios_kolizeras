import flet as ft

from logica.eliminar_cliente import eliminar_cliente
from logica.editar_cliente import editar_cliente
from logica.cargar_cliente import cargar_clientes
from ui.registro_ui import crear_dialogo_agregar_cliente
from utils.utils import crear_campo_texto, crear_boton


# ===============================================
#  region LOGICA CLIENTE
# ===============================================


def manejar_seleccion(e):
    # Obtener la fila seleccionada
    fila_seleccionada = e.control  # Esto devuelve la instancia de DataRow seleccionada

    # Alternar el estado de selección
    fila_seleccionada.selected = not fila_seleccionada.selected
    fila_seleccionada.update()  # Actualizar la fila en la interfaz

    if fila_seleccionada.selected:  # Verificar si la fila está seleccionada
        # Acceder al contenido de la primera celda (ID)
        btn_eliminar.disabled = False
        # id_seleccionado = fila_seleccionada.cells[0].content.value
        # print(f"El ID es: {id_seleccionado}")
    else:
        print("Fila deseleccionada")
    btn_eliminar.update()


def validar_campos(nombre, contacto):
    errores = {}
    if not nombre:
        errores["nombre"] = "Campo obligatorio"
    if not contacto:
        errores["contacto"] = "Campo obligatorio"
    return errores


def limpiar_campos():
    """Limpia los campos de texto."""
    txt_nombre.value = ""
    txt_contacto.value = ""
    txt_direccion.value = ""
    txt_nombre.error_text = ""
    txt_contacto.error_text = ""
    txt_nombre.update()
    txt_contacto.update()
    txt_direccion.update()


def obtener_cliente_seleccionado():
    """Obtiene el ID del cliente seleccionado."""
    for row in lista_clientes.rows:
        if row.selected:
            return row.cells[0].content.value
    return None


def editar_cliente_seleccionado(e):
    """Edita un cliente seleccionado."""
    selected_id = obtener_cliente_seleccionado()
    if not selected_id:
        print("No se ha seleccionado ningún cliente.")
        return

    errores = validar_campos(txt_nombre.value.strip(), txt_contacto.value.strip())
    if errores:
        txt_nombre.error_text = errores.get("nombre", "")
        txt_contacto.error_text = errores.get("contacto", "")
        txt_nombre.update()
        txt_contacto.update()
        return

    editar_cliente(
        selected_id,
        txt_nombre.value.strip(),
        txt_contacto.value.strip(),
        txt_direccion.value.strip(),
    )
    limpiar_campos()
    cargar_clientes_en_tabla()


def eliminar_cliente_seleccionado(e):
    """Elimina un cliente seleccionado."""
    selected_id = obtener_cliente_seleccionado()
    if not selected_id:
        print("No se ha seleccionado ningún cliente.")
        return
    eliminar_cliente(selected_id)
    cargar_clientes_en_tabla()


def cargar_clientes_en_tabla(e=None):
    """Carga los clientes en la tabla."""
    clientes = cargar_clientes()
    lista_clientes.rows = [
        ft.DataRow(
            on_select_changed=manejar_seleccion,
            cells=[
                ft.DataCell(ft.Text(str(cliente["id"]))),
                ft.DataCell(ft.Text(cliente["nombre"])),
                ft.DataCell(ft.Text(cliente["telefono"])),
                ft.DataCell(ft.Text(cliente["direccion"])),
            ],
            color="red",
        )
        for cliente in clientes
    ]
    lista_clientes.update()


# ===============================================
#     FIN DE LOGICA CLIENTE
# ===============================================


# ===============================================
# region ELEMENTOS INTERFAZ
# ===============================================
txt_nombre = crear_campo_texto("Nombre del cliente", "Ej: Alissa")
txt_contacto = crear_campo_texto("Contacto", "Ej: +56912345678")
txt_direccion = crear_campo_texto("Dirección", "Ej: Calle Principal #123")

btn_eliminar = crear_boton(
    "Eliminar", ft.icons.PERSON_REMOVE, eliminar_cliente_seleccionado, "red"
)
btn_editar = crear_boton(
    "Editar", ft.icons.EDIT_SQUARE, editar_cliente_seleccionado, "yellow"
)

btn_actualizar = ft.IconButton(icon=ft.Icons.REPLAY, on_click=cargar_clientes_en_tabla)


lista_clientes = ft.DataTable(
    show_checkbox_column=True,
    vertical_lines=ft.BorderSide(1, ft.Colors.GREY_300),
    columns=[
        ft.DataColumn(ft.Text("ID")),
        ft.DataColumn(ft.Text("Nombre")),
        ft.DataColumn(ft.Text("Contacto")),
        ft.DataColumn(ft.Text("Dirección")),
    ],
    show_bottom_border=True,
    rows=[],
    expand=True,
    border=ft.border.all(2, ft.Colors.GREY_300),
    # border_radius=4,
)

# ===============================================
# FIN DE LOS ELEMENTOS
# ===============================================


# region VISTA

vista_clientes = ft.Container(
    content=ft.Column(
        controls=[
            ft.Row(
                [
                    ft.Text("Clientes Registrados", size=25, weight="bold"),
                    ft.ElevatedButton(
                        text="Añadir",
                        icon=ft.Icons.PERSON_ADD,
                        icon_color="gray",
                        width=100,
                        style=ft.ButtonStyle(bgcolor="#2196F3", color="white"),
                        on_click=lambda e: crear_dialogo_agregar_cliente(e),
                    ),
                    btn_eliminar,
                    ft.ElevatedButton(
                        text="Editar",
                        icon=ft.Icons.EDIT,
                        style=ft.ButtonStyle(
                            bgcolor="yellow",
                            color="white",
                        ),
                        width=100,
                        disabled=True,
                    ),
                    btn_actualizar,
                ]
            ),
            lista_clientes,
        ],
        scroll=True,
        expand=True,
    ),
    border=ft.border.all(2, "#BBDEFB"),
    alignment=ft.alignment.center,
    expand=True,
    padding=20,
)
