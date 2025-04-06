import flet as ft
from logica.manejo_cliente import ManejoCliente
from ui.registro_ui import crear_dialogo_agregar_cliente
from utils.utils import crear_boton, DialogHandler


# ===============================================
# 1. CLASE PARA MANEJAR EL ESTADO Y COMPONENTES UI
# ===============================================
class ClienteUIState:
    def __init__(self):
        # Componentes de la interfaz
        # self.txt_nombre = crear_campo_texto("Nombre del cliente", "Ej: Alissa")
        # self.txt_contacto = crear_campo_texto("Contacto", "Ej: +56912345678")
        # self.txt_direccion = crear_campo_texto("Dirección", "Ej: Calle Principal #123")

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
# 3. VALIDACIONES CENTRALIZADAS
# ===============================================
# region VALIDACION
# class ValidadorCliente:
#     @staticmethod
#     def validar(nombre: str, contacto: str) -> dict:
#         errores = {}
#         if len(nombre.strip()) < 3:
#             errores["nombre"] = "Mínimo 3 caracteres"
#         if not contacto.strip().isdigit() or len(contacto.strip()) < 8:
#             errores["contacto"] = "Teléfono inválido"
#         return errores


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
                        weight="bold",
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
                    ft.DataCell(ft.Text(cliente["nombre"])),
                    ft.DataCell(ft.Text(cliente["telefono"])),
                    ft.DataCell(ft.Text(cliente["direccion"])),
                ],
                on_select_changed=lambda e, s=state: _manejar_seleccion(e, s),
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

    def guardar_cambios(datos_actualizados):
        try:
            state.manejo_cliente.editar_cliente(
                datos_actualizados["id"],
                datos_actualizados["nombre"],
                datos_actualizados["telefono"],
                datos_actualizados["direccion"],
            )
            _cargar_clientes(e, state)  # Refrescar la tabla
        except Exception as error:
            print(f"Error al editar cliente: {error}")

    DialogHandler.crear_dialogo_edicion(
        e.page, cliente_data=cliente_data, on_edit=guardar_cambios
    )


# DESHACER LOS CAMBIOS PARA LA EDICION DE CLIENTES YA QUE HAY ERRORES
# HACER DESDE 0 PARA CORREGIR LOS ERRORES


# ===============================================
# 5. INICIALIZACIÓN (Reemplaza las variables globales)
# ===============================================
cliente_state = ClienteUIState()
vista_clientes = setup_cliente_ui(cliente_state)

# # ===============================================
# #  region LOGICA CLIENTE
# # ===============================================
# manejo_cliente = ManejoCliente()


# def manejar_seleccion(e):
#     # Obtener la fila seleccionada
#     fila_seleccionada = e.control  # Esto devuelve la instancia de DataRow seleccionada

#     # Alternar el estado de selección
#     fila_seleccionada.selected = not fila_seleccionada.selected
#     fila_seleccionada.update()  # Actualizar la fila en la interfaz

#     if fila_seleccionada.selected:  # Verificar si la fila está seleccionada
#         # Acceder al contenido de la primera celda (ID)
#         btn_eliminar.disabled = False
#         btn_editar.disabled = False
#         # id_seleccionado = fila_seleccionada.cells[0].content.value
#         # print(f"El ID es: {id_seleccionado}")
#     else:
#         btn_eliminar.disabled = True
#         btn_editar.disabled = True
#         print("Fila deseleccionada")
#     btn_eliminar.update()
#     btn_editar.update()


# def validar_campos(nombre, contacto):
#     errores = {}
#     if not nombre or len(nombre) < 5:
#         errores["nombre"] = "Campo obligatorio"
#     if not contacto:
#         errores["contacto"] = "Campo obligatorio"
#     return errores


# def limpiar_campos():
#     """Limpia los campos de texto."""
#     txt_nombre.value = ""
#     txt_contacto.value = ""
#     txt_direccion.value = ""
#     txt_nombre.error_text = ""
#     txt_contacto.error_text = ""
#     txt_nombre.update()
#     txt_contacto.update()
#     txt_direccion.update()


# def obtener_cliente_seleccionado():
#     """Obtiene el ID del cliente seleccionado."""
#     for row in lista_clientes.rows:
#         if row.selected:
#             return row.cells[0].content.value
#     return None


# def editar_cliente_seleccionado(e):
#     """Edita un cliente seleccionado."""
#     selected_id = obtener_cliente_seleccionado()
#     if not selected_id:
#         print("No se ha seleccionado ningún cliente.")
#         return

#     errores = validar_campos(txt_nombre.value.strip(), txt_contacto.value.strip())
#     if errores:
#         txt_nombre.error_text = errores.get("nombre", "")
#         txt_contacto.error_text = errores.get("contacto", "")
#         txt_nombre.update()
#         txt_contacto.update()
#         return

#     manejo_cliente.editar_cliente(
#         selected_id,
#         txt_nombre.value.strip(),
#         txt_contacto.value.strip(),
#         txt_direccion.value.strip(),
#     )
#     limpiar_campos()
#     cargar_clientes_en_tabla()


# def eliminar_cliente_seleccionado(e):
#     """Elimina un cliente seleccionado."""
#     selected_id = obtener_cliente_seleccionado()
#     if not selected_id:
#         print("No se ha seleccionado ningún cliente.")
#         return
#     manejo_cliente.eliminar_cliente(selected_id)
#     cargar_clientes_en_tabla()


# def cargar_clientes_en_tabla(e=None):
#     """Carga los clientes en la tabla."""
#     clientes = manejo_cliente.cargar_clientes()
#     lista_clientes.rows = [
#         ft.DataRow(
#             on_select_changed=manejar_seleccion,
#             cells=[
#                 ft.DataCell(ft.Text(str(cliente["id"]))),
#                 ft.DataCell(ft.Text(cliente["nombre"])),
#                 ft.DataCell(ft.Text(cliente["telefono"])),
#                 ft.DataCell(ft.Text(cliente["direccion"])),
#             ],
#             # color="red",
#         )
#         for cliente in clientes
#     ]
#     lista_clientes.update()


# # ===============================================
# #     FIN DE LOGICA CLIENTE
# # ===============================================


# # ===============================================
# # region DIALOGO DE CONFIRMACION
# # ===============================================
# def abrir_dialogo_confirmacion(e):
#     """Abre un diálogo modal de confirmación antes de eliminar un cliente."""

#     def confirmar_eliminacion(e):
#         """Confirma la eliminación del cliente."""
#         # eliminar_cliente_seleccionado(e)
#         dialogo.open = False
#         e.page.update()

#     def cancelar_eliminacion(e):
#         """Cierra el diálogo sin eliminar."""
#         e.page.overlay[-1].open = False
#         e.page.update()
#         e.page.overlay.pop()

#     # Crear el diálogo modal de confirmación
#     dialogo = ft.AlertDialog(
#         modal=True,
#         title=ft.Text("Confirmar Eliminación", text_align="center", weight="bold"),
#         content=ft.Text("¿Estás seguro de que deseas eliminar este cliente?", size=30),
#         actions=[
#             ft.TextButton("Eliminar", on_click=confirmar_eliminacion),
#             ft.TextButton("Cancelar", on_click=cancelar_eliminacion),
#         ],
#         actions_alignment=ft.MainAxisAlignment.END,
#     )


#     # Abrir el diálogo
#     e.control.page.overlay.append(dialogo)
#     dialogo.open = True
#     btn_eliminar.disabled = True
#     e.control.page.update()


# # ===============================================
# # region DIALOGO DE EDICION DE CLIENTE
# # ===============================================
# def abrir_dialogo_edicion(e):
#     """Abre un diálogo modal para editar un cliente."""

#     def cancelar_edicion(e):
#         e.page.overlay[-1].open = False
#         e.page.update()
#         e.page.overlay.pop()

#     dialogo = ft.AlertDialog(
#         modal=True,
#         title=ft.Text("Editar Cliente", text_align="center", weight="bold"),
#         content=ft.Column(
#             controls=[
#                 txt_nombre,
#                 txt_contacto,
#                 txt_direccion,
#             ],
#             spacing=30,
#             width=400,
#             horizontal_alignment=ft.CrossAxisAlignment.CENTER,
#             height=350,
#         ),
#         actions=[
#             ft.TextButton("Guardar", on_click=editar_cliente_seleccionado),
#             ft.TextButton("Cancelar", on_click=cancelar_edicion),
#         ],
#     )
#     # Abrir el diálogo
#     e.control.page.overlay.append(dialogo)
#     dialogo.open = True
#     btn_eliminar.disabled = True
#     e.control.page.update()


# # ===============================================
# # region ELEMENTOS INTERFAZ
# # ===============================================
# txt_nombre = crear_campo_texto("Nombre del cliente", "Ej: Alissa")
# txt_contacto = crear_campo_texto("Contacto", "Ej: +56912345678")
# txt_direccion = crear_campo_texto("Dirección", "Ej: Calle Principal #123")

# btn_eliminar = crear_boton(
#     "Eliminar", ft.icons.PERSON_REMOVE, abrir_dialogo_confirmacion, "red"
# )
# btn_editar = crear_boton(
#     "Editar", ft.icons.EDIT_SQUARE, abrir_dialogo_edicion, "yellow"
# )


# btn_actualizar = ft.IconButton(icon=ft.Icons.REPLAY, on_click=cargar_clientes_en_tabla)


# lista_clientes = ft.DataTable(
#     show_checkbox_column=True,
#     # vertical_lines=ft.BorderSide(1, ft.Colors.GREY_300),
#     columns=[
#         ft.DataColumn(ft.Text("ID")),
#         ft.DataColumn(ft.Text("Nombre")),
#         ft.DataColumn(ft.Text("Contacto")),
#         ft.DataColumn(ft.Text("Dirección")),
#     ],
#     rows=[],
#     expand=True,
#     # border=ft.border.only(
#     #     left=ft.border.BorderSide(1, ft.Colors.GREY_300),
#     #     right=ft.border.BorderSide(1, ft.Colors.GREY_300),
#     #     bottom=ft.border.BorderSide(1, ft.Colors.GREY_300),
#     # ),
# )

# # ===============================================
# # FIN DE LOS ELEMENTOS
# # ===============================================


# # region VISTA

# vista_clientes = ft.Container(
#     content=ft.Column(
#         controls=[
#             ft.Text("Clientes Registrados", size=25, weight="bold"),
#             ft.Row(
#                 [
#                     ft.ElevatedButton(
#                         text="Añadir",
#                         icon=ft.Icons.PERSON_ADD,
#                         icon_color="gray",
#                         width=100,
#                         style=ft.ButtonStyle(bgcolor="#2196F3", color="white"),
#                         on_click=lambda e: crear_dialogo_agregar_cliente(e),
#                     ),
#                     btn_eliminar,
#                     btn_editar,
#                     btn_actualizar,
#                 ],
#                 alignment=ft.MainAxisAlignment.CENTER,
#             ),
#             # ft.Divider(height=20),
#             ft.Container(
#                 content=lista_clientes,
#                 border=ft.border.all(1, ft.Colors.GREY_300),
#                 border_radius=5,
#                 padding=10,
#                 expand=True,
#             ),
#         ],
#         horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
#         scroll=ft.ScrollMode.AUTO,
#         spacing=20,
#         expand=True,
#     )
# )
