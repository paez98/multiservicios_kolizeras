import flet as ft
from logica import cargar_clientes, guardar_cliente, eliminar_cliente, editar_cliente

# ===============================================
#     ELEMENTOS DE LA INTERFAZ (Solo gráficos)
# ===============================================
txt_nombre = ft.TextField(
    label="Nombre del cliente",
    width=300,
    border_color="#2196F3",
    hint_text="Ej: Alissa"
)
txt_contacto = ft.TextField(
    label="Contacto",
    width=300,
    border_color="#2196F3",
    hint_text="Ej: +56912345678"
)
txt_direccion = ft.TextField(
    label="Dirección",
    width=300,
    border_color="#2196F3",
    hint_text="Ej: Calle Principal #123"
)

btn_eliminar = ft.ElevatedButton(
    text='Eliminar',
    icon=ft.icons.DELETE_FOREVER,
    width=200,
    height=50,
    style=ft.ButtonStyle(bgcolor="red", color="white"),
    on_click=lambda e: eliminar_cliente_seleccionado(e)
)

btn_guardar = ft.ElevatedButton(
    text='Guardar',
    icon=ft.icons.SAVE_SHARP,
    width=200,
    height=50,
    style=ft.ButtonStyle(bgcolor="#2196F3", color="white"),
    on_click=lambda e: guardar_cliente_nuevo(e)
)

btn_editar = ft.ElevatedButton(
    text='Editar',
    icon=ft.icons.EDIT_SQUARE,
    width=200,
    height=50,
    style=ft.ButtonStyle(bgcolor="yellow", color="dark-yellow"),
    on_click=lambda e: editar_cliente_seleccionado(e)
)

lista_clientes = ft.DataTable(
    columns=[
        ft.DataColumn(ft.Text("ID")),
        ft.DataColumn(ft.Text("Nombre")),
        ft.DataColumn(ft.Text("Contacto")),
        ft.DataColumn(ft.Text("Dirección")),
    ],
    rows=[],
    expand=True
)

vista_clientes = ft.Container(
    content=ft.Row(
        controls=[
            ft.Column(
                controls=[
                    ft.Text('Registrar cliente', size=30, weight=200),
                    txt_nombre,
                    txt_contacto,
                    txt_direccion,
                    btn_guardar,
                    btn_eliminar,
                    btn_editar
                ]
            ),
            ft.Column([lista_clientes], expand=True)
        ],
        spacing=40,
        expand=True
    ),
    border=ft.border.all(2, "#BBDEFB"),
    expand=True
)


# ===============================================
#     FUNCIONES DE LA LÓGICA
# ===============================================
def cargar_clientes_en_tabla():
    """Carga los clientes en la tabla."""
    clientes = cargar_clientes()
    lista_clientes.rows.clear()
    for cliente in clientes:
        lista_clientes.rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(cliente["id"]))),
                    ft.DataCell(ft.Text(cliente["nombre"])),
                    ft.DataCell(ft.Text(cliente["telefono"])),
                    ft.DataCell(ft.Text(cliente["direccion"]))
                ]
            )
        )
    lista_clientes.update()


def guardar_cliente_nuevo(e):
    """Guarda un nuevo cliente."""
    nombre = txt_nombre.value.strip()
    contacto = txt_contacto.value.strip()
    direccion = txt_direccion.value.strip()

    if not nombre or not contacto:
        txt_nombre.error_text = "Campo obligatorio" if not nombre else ""
        txt_contacto.error_text = "Campo obligatorio" if not contacto else ""
        txt_nombre.update()
        txt_contacto.update()
        return

    guardar_cliente(nombre, contacto, direccion)
    txt_nombre.value = ""
    txt_contacto.value = ""
    txt_direccion.value = ""
    txt_nombre.error_text = ""
    txt_contacto.error_text = ""
    txt_nombre.update()
    txt_contacto.update()
    txt_direccion.update()
    cargar_clientes_en_tabla()


def eliminar_cliente_seleccionado(e):
    """Elimina un cliente seleccionado."""
    selected_id = None
    for row in lista_clientes.rows:
        if row.selected:
            selected_id = row.cells[0].content.value
            break

    if not selected_id:
        print("No se ha seleccionado ningún cliente.")
        return

    eliminar_cliente(selected_id)
    cargar_clientes_en_tabla()


def editar_cliente_seleccionado(e):
    """Edita un cliente seleccionado."""
    selected_id = None
    for row in lista_clientes.rows:
        if row.selected:
            selected_id = row.cells[0].content.value
            break

    if not selected_id:
        print("No se ha seleccionado ningún cliente.")
        return

    nombre = txt_nombre.value.strip()
    contacto = txt_contacto.value.strip()
    direccion = txt_direccion.value.strip()

    if not nombre or not contacto:
        txt_nombre.error_text = "Campo obligatorio" if not nombre else ""
        txt_contacto.error_text = "Campo obligatorio" if not contacto else ""
        txt_nombre.update()
        txt_contacto.update()
        return

    editar_cliente(selected_id, nombre, contacto, direccion)
    txt_nombre.value = ""
    txt_contacto.value = ""
    txt_direccion.value = ""
    txt_nombre.error_text = ""
    txt_contacto.error_text = ""
    txt_nombre.update()
    txt_contacto.update()
    txt_direccion.update()
    cargar_clientes_en_tabla()


# ===============================================
#     INICIALIZAR LA APLICACIÓN
# ===============================================
def main(page: ft.Page):
    page.title = "Gestión de Clientes"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.scroll = "adaptive"

    # Cargar clientes al iniciar la aplicación
    cargar_clientes_en_tabla()

    # Agregar la vista principal
    page.add(vista_clientes)


# Ejecutar la aplicación
if __name__ == "__main__":
    ft.app(target=main)
