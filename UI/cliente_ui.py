import flet as ft
from logica.crear_cliente import guardar_cliente
from logica.eliminar_cliente import eliminar_cliente
from logica.editar_cliente import editar_cliente
from logica.cargar_cliente import cargar_clientes
from ui.registro_ui import crear_dialogo_agregar_cliente
from utils import crear_campo_texto, crear_boton, actualizar_tabla


# ===============================================
#  region LOGICA CLIENTE
# ===============================================


def validar_campos(nombre, contacto):
    errores = {}
    if not nombre:
        errores["nombre"] = "Campo obligatorio"
    if not contacto:
        errores[contacto] = "Campo obligatorio"
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


def guardar_cliente_nuevo():
    errores = validar_campos(txt_nombre.value.strip(), txt_contacto.value.strip())
    if errores:
        txt_nombre.error_text = errores.get("nombre", "")
        txt_contacto.error_text = errores.get("contacto", "")
        txt_nombre.update()
        txt_contacto.update()
        return
    guardar_cliente(
        txt_direccion.value.strip(),
        txt_contacto.value.strip(),
        txt_direccion.value.strip(),
    )
    limpiar_campos()
    cargar_clientes_en_tabla()


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


def cargar_clientes_en_tabla():
    """Carga los clientes en la tabla."""
    clientes = cargar_clientes()
    lista_clientes.rows = [
        ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(str(cliente["id"]))),
                ft.DataCell(ft.Text(cliente["nombre"])),
                ft.DataCell(ft.Text(cliente["telefono"])),
                ft.DataCell(ft.Text(cliente["direccion"])),
            ],
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

btn_guardar = crear_boton(
    "Guardar", ft.icons.SAVE_SHARP, guardar_cliente_nuevo, "#2196F3"
)
btn_eliminar = crear_boton(
    "Eliminar", ft.icons.DELETE_FOREVER, eliminar_cliente_seleccionado, "red"
)
btn_editar = crear_boton(
    "Editar", ft.icons.EDIT_SQUARE, editar_cliente_seleccionado, "yellow"
)

lista_clientes = ft.DataTable(
    bgcolor="yellow",
    border=ft.border.all(2, "red"),
    border_radius=10,
    vertical_lines=ft.border.BorderSide(3, "blue"),
    horizontal_lines=ft.border.BorderSide(1, "green"),
    sort_column_index=0,
    sort_ascending=True,
    heading_row_color=ft.Colors.BLACK12,
    heading_row_height=100,
    data_row_color={"hovered": "0x30FF0000"},
    show_checkbox_column=True,
    divider_thickness=0,
    column_spacing=200,
    columns=[
        ft.DataColumn(ft.Text("ID")),
        ft.DataColumn(ft.Text("Nombre")),
        ft.DataColumn(ft.Text("Contacto")),
        ft.DataColumn(ft.Text("Dirección")),
    ],
    show_bottom_border=True,
    rows=[],
    expand=True,
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
                        on_click=lambda e: crear_dialogo_agregar_cliente(
                            e, actualizar_tabla
                        ),
                    ),
                    ft.ElevatedButton(
                        text="Eliminar",
                        icon=ft.Icons.PERSON_REMOVE_ROUNDED,
                        style=ft.ButtonStyle(bgcolor="red", color="white"),
                        width=100,
                        disabled=True,
                    ),
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
