import flet as ft
from logica.manejo_cliente import ManejoCliente
from ui.registro_ui import crear_dialogo_agregar_cliente
from utils.utils import crear_boton, DialogHandler


# ===============================================
# 1. CLASE PARA MANEJAR EL ESTADO Y COMPONENTES UI
# ===============================================
class ClienteUIState:
    def __init__(self):
        # Botones
        self.btn_eliminar = crear_boton("Eliminar", ft.Icons.PERSON_REMOVE, None, "red")
        self.btn_agregar = crear_boton("Añadir", ft.Icons.PERSON_ADD, None, "green")
        self.btn_editar = crear_boton("Editar", ft.Icons.EDIT_SQUARE, None, "yellow")
        self.btn_actualizar = ft.IconButton(icon=ft.Icons.REPLAY, on_click=None)

        # DataTable Clientes
        self.lista_clientes = ft.DataTable(
            show_checkbox_column=True,
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Nombre")),
                ft.DataColumn(ft.Text("Contacto")),
                ft.DataColumn(ft.Text("Dirección")),
            ],
            rows=[],
            expand=True,
            border=ft.border.all(1, ft.Colors.GREY_300),
        )
        # Dependencias
        self.manejo_cliente = ManejoCliente()


# ===============================================
# 4. FUNCIONES PRINCIPALES REORGANIZADAS
# ===============================================
# region VIEW CLIENTE
def setup_cliente_ui(state: ClienteUIState):
    # Configurar eventos
    state.btn_eliminar.on_click = lambda e: _eliminar_cliente(e, state)
    state.btn_editar.on_click = lambda e: edit(e, state)
    state.btn_actualizar.on_click = lambda e: _cargar_clientes(e, state)
    state.btn_agregar.on_click = lambda e: crear_dialogo_agregar_cliente(e)
    state.btn_agregar.disabled = False

    # Construir vista
    return ft.Column(
        controls=[
            ft.Column(
                controls=[
                    ft.Text(
                        "Clientes Registrados",
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
                    controls=[state.lista_clientes],
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


# ===============================================
# 5. FUNCIONES INTERNAS - (Los "ayudantes secretos")
# ===============================================
# region LOGCIA


def _cargar_clientes(e, state: ClienteUIState):
    # Tu lógica actual usando state.lista_clientes y state.manejo_cliente
    try:
        clientes = state.manejo_cliente.cargar_clientes()
        state.lista_clientes.rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(cliente.get("id")))),
                    ft.DataCell(ft.Text(cliente.get("name", ""))),
                    ft.DataCell(ft.Text(cliente.get("phone", ""))),
                    ft.DataCell(ft.Text(cliente.get("address", ""))),
                ],
                on_select_changed=lambda ev, s=state: _manejar_seleccion(ev, s),
            )
            for cliente in clientes
        ]
        state.lista_clientes.update()
    except Exception as e:
        print(f"Error al cargar los clientes {e}")


def _manejar_seleccion(e, state: ClienteUIState):
    """Habilita/deshabilita botones cuando se selecciona una fila"""
    fila = e.control
    fila.selected = not fila.selected
    fila.update()
    hay_seleccion = any(row.selected for row in state.lista_clientes.rows)
    print(hay_seleccion)
    state.btn_editar.disabled = not hay_seleccion
    state.btn_eliminar.disabled = not hay_seleccion
    state.btn_eliminar.update()
    state.btn_editar.update()


def _eliminar_cliente(e, state: ClienteUIState):
    """Maneja todo el proceso de eliminación de un cliente"""
    cliente_id = obtener_datos(state, True)

    if not cliente_id:
        print("Ningún cliente seleccionado")
        return

    def confirmar_eliminacion(e):
        try:
            state.manejo_cliente.eliminar_cliente(cliente_id)
            _cargar_clientes(e, state)
            e.page.overlay[-1].open = False
            e.page.update()
        except Exception as e:
            print(f"Error al eliminar el cliente: {e}")

    DialogHandler.crear_dialogo_confirmacion(
        page=e.page,
        titulo="Confirmar Eliminación",
        mensaje="¿Estás seguro de que deseas eliminar este cliente?",
        on_confirm=confirmar_eliminacion,
    )


def obtener_datos(state: ClienteUIState, solo_id: bool = False):
    for row in state.lista_clientes.rows:
        if row.selected:
            if solo_id:  # Modo eliminación
                return row.cells[0].content.value
            else:  # Modo edición
                return {
                    "Id": row.cells[0].content.value,
                    "Nombre": row.cells[1].content.value,
                    "Telefono": row.cells[2].content.value,
                    "Direccion": row.cells[3].content.value,
                }
    return None


def edit(e, state: ClienteUIState):
    cliente_data = obtener_datos(state)
    if not cliente_data:
        print("Ningún cliente seleccionado")
        return

    def actualizar_lista():
        _cargar_clientes(e, state)

    DialogHandler.crear_dialogo_edicion(
        e.page,
        cliente_data=cliente_data,
        manejo_cliente=state.manejo_cliente,
        on_edit=actualizar_lista,
    )


# ===============================================
# 5. INICIALIZACIÓN (Reemplaza las variables globales)
# ===============================================
cliente_state = ClienteUIState()
vista_clientes = setup_cliente_ui(cliente_state)
