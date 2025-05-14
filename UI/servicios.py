import flet as ft
from logica.manejo_servicio import ManejoServicio
from utils.utils import crear_boton, DialogHandler
from ui.registro_ui import crear_dialogo_agregar_servicio

manejo_servicio = ManejoServicio()


class ServicioUiState:
    def __init__(self):
        self.manejo = ManejoServicio()

        self.btn_eliminar = crear_boton("Eliminar", ft.Icons.DELETE, None, "red")
        self.btn_agregar = crear_boton("Añadir", ft.Icons.ADD, None, "green")
        self.btn_agregar.disabled = False
        self.btn_editar = crear_boton("Editar", ft.Icons.EDIT_SQUARE, None, "yellow")
        self.btn_actualizar = ft.IconButton(icon=ft.Icons.REPLAY, on_click=None)

        # Datatable de servicios
        self.lista_servicios = ft.DataTable(
            show_checkbox_column=True,
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Descripción")),
                ft.DataColumn(ft.Text("Precio")),
            ],
            rows=[],
            expand=True,
            border=ft.border.all(1, ft.Colors.GREY_300),
        )


# region VISTA
def setup_servicio_ui(state: ServicioUiState):
    state.btn_eliminar.on_click = lambda e: _eliminar_servicio(e, state)
    state.btn_editar.on_click = lambda e: edit(e, state)
    state.btn_agregar.on_click = lambda e: crear_dialogo_agregar_servicio(e)
    state.btn_actualizar.on_click = lambda e: _cargar_servicio(e, state)
    return ft.Column(
        controls=[
            ft.Column(
                controls=[
                    ft.Text(
                        "Servicios registrados",
                        size=25,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Row(
                        controls=[
                            state.btn_agregar,
                            state.btn_eliminar,
                            state.btn_editar,
                            state.btn_actualizar,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            ft.Divider(),
            ft.Container(
                content=ft.Column(
                    controls=[state.lista_servicios],
                    scroll=ft.ScrollMode.AUTO,
                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                ),
                # border=ft.border.all(1, "#E1BEE7"),
                border_radius=10,
                padding=10,
                expand=True,
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        expand=True,
    )


# region LOGICA
def _cargar_servicio(e, state: ServicioUiState):
    # Tu lógica actual usando state.lista_clientes y state.manejo_cliente
    try:
        clientes = state.manejo.cargar_servicios()
        state.lista_servicios.rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(cliente.get("id")))),
                    ft.DataCell(ft.Text(cliente["descripcion"])),
                    ft.DataCell(ft.Text(cliente["precio"])),
                ],
                on_select_changed=lambda e, s=state: _manejar_seleccion(e, s),
            )
            for cliente in clientes
        ]
        state.lista_servicios.update()
    except Exception as e:
        print(f"Error al cargar los servicios {e}")


def _manejar_seleccion(e, state: ServicioUiState):
    """Habilita/deshabilita botones cuando se selecciona una fila"""
    fila = e.control
    fila.selected = not fila.selected
    fila.update()
    hay_seleccion = any(row.selected for row in state.lista_servicios.rows)
    print(hay_seleccion)
    state.btn_editar.disabled = not hay_seleccion
    state.btn_eliminar.disabled = not hay_seleccion
    state.btn_eliminar.update()
    state.btn_editar.update()


def obtener_datos(state: ServicioUiState, solo_id: bool = False):
    for row in state.lista_servicios.rows:
        if row.selected:
            if solo_id:  # Modo eliminación
                return row.cells[0].content.value
            else:  # Modo edición
                return {
                    "Id": row.cells[0].content.value,
                    "Descripcion": row.cells[1].content.value,
                    "Precio": row.cells[2].content.value,
                }
    return None


def _eliminar_servicio(e, state: ServicioUiState):
    """Maneja todo el proceso de eliminación de un cliente"""
    servicio_id = obtener_datos(state, True)

    if not servicio_id:
        print("Ningún cliente seleccionado")
        return

    def confirmar_eliminacion(e):
        try:
            state.manejo.eliminar_servicio(servicio_id)
            # _cargar_servicio(e, state)
            e.page.overlay[-1].open = False
            e.page.update()
        except Exception as e:
            print(f"Error al eliminar el cliente: {e}")

    DialogHandler.crear_dialogo_confirmacion(
        page=e.page,
        titulo="Confirmar Eliminación",
        mensaje="¿Estás seguro de que deseas eliminar este servicio?",
        on_confirm=confirmar_eliminacion,
    )


def edit(e, state: ServicioUiState):
    servicio_data = obtener_datos(state)
    if not servicio_data:
        print("Ningún cliente seleccionado")
        return

    def guardar_cambios(datos_actualizados):
        try:
            state.manejo.editar_servicio(
                datos_actualizados["id"],
                datos_actualizados["descripcion"],
                datos_actualizados["precio"],
            )
            # _cargar_servicio(e, state)  # Refrescar la tabla
        except Exception as error:
            print(f"Error al editar cliente: {error}")

    DialogHandler.crear_dialogo_edicion_servicio(
        e.page, servicio_data=servicio_data, on_edit=guardar_cambios
    )


servicio_state = ServicioUiState()
lista_servicios = setup_servicio_ui(servicio_state)
