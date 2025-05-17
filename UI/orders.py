import flet as ft
from logica.manejo_servicio import ManejoServicio
from logica.manejo_ordenes import ManejoOrdenes
from logica.manejo_cliente import ManejoCliente


class OrdenContainer(ft.Container):
    def __init__(
            self,
            orden_id,
            cliente,
            servicio,
            vehiculo,
            descripcion,
            fecha_orden,
            estado,
    ):
        super().__init__(
            border_radius=15,
            on_hover=self._on_hover,
            on_click=self.abrir_dialogo,
            animate_scale=ft.Animation(200, ft.AnimationCurve.EASE_IN_CIRC),
        )
        self.manejo_orden = ManejoOrdenes()
        self.manejo_cliente = ManejoCliente()
        self.manejo_servicio = ManejoServicio()

        self.orden_id = orden_id
        self.cliente = cliente
        self.servicio = servicio
        self.vehiculo = vehiculo
        self.descripcion = descripcion
        self.fecha_orden = fecha_orden
        self.estado = estado

        # --- Controles para el base_content---
        self._txt_servicio_card = ft.Text(
            self.servicio,
            theme_style=ft.TextThemeStyle.TITLE_LARGE,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER,
        )
        self._txt_cliente_card = ft.Text(
            self.cliente,
            theme_style=ft.TextThemeStyle.TITLE_MEDIUM,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER,
        )
        self._txt_vehiculo_card = ft.Text(
            self.vehiculo, theme_style=ft.TextThemeStyle.TITLE_MEDIUM
        )
        self._txt_descripcion_card = ft.Text(
            self.descripcion,
            overflow=ft.TextOverflow.ELLIPSIS,
            max_lines=3,
            no_wrap=False,
            text_align=ft.TextAlign.CENTER,
        )
        self._txt_fecha_orden_card = ft.Text(self.fecha_orden)
        self._txt_estado_card = ft.Text(self.estado, text_align=ft.TextAlign.RIGHT)

        self.base_content = ft.Card(
            elevation=5,
            content=ft.Container(
                content=ft.Column(
                    [
                        # Servicio a realizar
                        self._txt_servicio_card,
                        self._txt_cliente_card,
                        # Vehiculo
                        self._txt_vehiculo_card,
                        self._txt_descripcion_card,
                        self._txt_fecha_orden_card,
                        # Estado
                        self._txt_estado_card,
                    ],
                    spacing=5,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=15,
            ),
        )

        self.content = self.base_content

        self._txt_dialog_vehiculo_title = ft.Text(
            f"Orden N⁰ {self.orden_id}:    {self.vehiculo}", weight=ft.FontWeight.BOLD
        )
        self._txt_dialog_servicio_value = ft.Text(self.servicio)
        self._txt_dialog_cliente_value = ft.Text(self.cliente)
        self._txt_dialog_descripcion_value = ft.Text(self.descripcion)
        self._txt_dialog_fecha_orden_value = ft.Text(self.fecha_orden)
        self._txt_dialog_estado_value = ft.Text(self.estado)

        # -----DIALOGO DETALLES ORDEN-----
        self.detalles_dialogo = ft.AlertDialog(
            modal=True,
            title=self._txt_dialog_vehiculo_title,
            content=ft.Container(
                width=400,
                padding=10,
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Container(
                                    content=ft.Column(
                                        [
                                            ft.Row(
                                                [
                                                    ft.Icon(
                                                        ft.Icons.MISCELLANEOUS_SERVICES
                                                    ),
                                                    ft.Text(
                                                        "Servicio:",
                                                        weight=ft.FontWeight.BOLD,
                                                    ),
                                                ]
                                            ),
                                            self._txt_dialog_servicio_value,  # Usar la referencia
                                        ]
                                    )
                                ),
                                ft.Container(
                                    content=ft.Column(
                                        [
                                            ft.Row(
                                                [
                                                    ft.Icon(ft.Icons.PERSON),
                                                    ft.Text(
                                                        "Cliente:",
                                                        weight=ft.FontWeight.BOLD,
                                                    ),
                                                ]
                                            ),
                                            self._txt_dialog_cliente_value,  # Usar la referencia
                                        ]
                                    )
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_AROUND,
                        ),
                        # Sección Servicio
                        ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                        # Sección Descripción
                        ft.Row(
                            [
                                ft.Icon(ft.Icons.DESCRIPTION),
                                ft.Text(
                                    "Descripción:",
                                    weight=ft.FontWeight.BOLD,
                                ),
                            ]
                        ),
                        ft.Container(
                            content=ft.Column(
                                [
                                    self._txt_dialog_descripcion_value
                                ],  # Usar la referencia
                                scroll=ft.ScrollMode.ADAPTIVE,
                            ),
                            padding=ft.padding.all(8),
                            height=150,
                            border_radius=5,
                        ),
                        ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                        # Sección Fecha Límite
                        ft.Row(
                            [
                                ft.Icon(ft.Icons.EVENT_AVAILABLE),
                                ft.Text("Fecha de Orden:", weight=ft.FontWeight.BOLD),
                            ]
                        ),
                        self._txt_dialog_fecha_orden_value,  # Usar la referencia
                        ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                        ft.Row(
                            [
                                ft.Icon(ft.Icons.TIMELAPSE),
                                ft.Text("Estado de Orden:", weight=ft.FontWeight.BOLD),
                            ]
                        ),
                        self._txt_dialog_estado_value,  # Usar la referencia
                    ],
                    spacing=5,
                    scroll=ft.ScrollMode.ADAPTIVE,
                    height=400,
                ),
            ),
            actions=[
                ft.TextButton(
                    "Eliminar",
                    style=ft.ButtonStyle(color=ft.Colors.RED_300),
                    on_click=lambda e: self.eliminar_orden(e),
                ),
                ft.TextButton(
                    "Editar",
                    style=ft.ButtonStyle(color=ft.Colors.YELLOW_300),
                    on_click=lambda e: self.abrir_dialogo_edicion(e),
                ),
                ft.TextButton("Cerrar", on_click=self.close_dialogo),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        # ----- CONTROLES PARA EL DIALOGO DE EDICION -----
        # Los hacemos atributos para poder acceder a sus valores al guardar
        self._edit_dd_cliente = ft.Dropdown(
            label="Cliente", enable_filter=True, editable=True, options=[], expand=True
        )
        self._edit_dd_servicio = ft.Dropdown(
            label="Servicio", enable_filter=True, editable=True, options=[], expand=True
        )
        self._edit_txt_vehiculo = ft.TextField(label="Vehículo")
        self._edit_txt_descripcion = ft.TextField(
            label="Descripción", multiline=True, max_lines=7
        )
        self._edit_txt_estado = ft.TextField(label="Estado")

        # ----- DIALOGO DE EDICION -----
        self.dialogo_edicion = ft.AlertDialog(
            modal=True,
            title=ft.Text("Editar Orden"),
            content=ft.Container(
                width=500,  # Puede ser un poco más ancho para el formulario
                content=ft.Column(
                    [
                        ft.Row([self._edit_dd_cliente, self._edit_dd_servicio]),
                        self._edit_txt_vehiculo,
                        self._edit_txt_descripcion,
                        self._edit_txt_estado,
                    ],
                    spacing=15,
                    scroll=ft.ScrollMode.ADAPTIVE,
                ),
            ),
            actions=[
                ft.ElevatedButton(
                    "Guardar Cambios", on_click=lambda e: self._guardar_cambios(e)
                ),
                ft.TextButton(
                    "Cancelar", on_click=lambda e: self.close_dialogo(e)
                ),  # Handler para cancelar
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

    # -----METODOS-----

    def _on_hover(self, e):
        container = e.control
        hover = e.data == "true"
        container.scale = 1.1 if hover else 1.0
        container.elevation = 20 if hover else 5  # Ajustar elevación con hover
        container.update()

    def _cargar_dd_edicion(self):
        clientes = self.manejo_cliente.cargar_clientes()
        servicios = self.manejo_servicio.cargar_servicios()

        self._edit_dd_cliente.options = [
            ft.dropdown.Option(
                key=cliente.get("id", ""), text=cliente.get("nombre", "")
            )
            for cliente in clientes
        ]

        self._edit_dd_servicio.options = [
            ft.dropdown.Option(
                key=servicio.get("id", ""), text=servicio.get("descripcion", "")
            )
            for servicio in servicios
        ]

    def abrir_dialogo(self, e):
        e.control.page.overlay.append(self.detalles_dialogo)
        self.detalles_dialogo.open = True
        e.control.page.update()

    def abrir_dialogo_edicion(self, e):
        self.close_dialogo(e)

        orden_data = self.manejo_orden.cargar_orden_id(self.orden_id)

        if orden_data:

            # Rellenar los campos del formulario de edición con los datos frescos
            self._edit_dd_cliente.value = str(
                orden_data.get("cliente", "")
            )  # Asume que el ID del cliente viene en 'cliente'
            self._edit_dd_servicio.value = str(
                orden_data.get("servicio", "")
            )  # Asume que el ID del servicio viene en 'servicio'
            self._edit_txt_vehiculo.value = orden_data.get("vehiculo", "")
            self._edit_txt_descripcion.value = orden_data.get("descripcion", "")
            self._edit_txt_estado.value = orden_data.get("estado", "")

            self.dialogo_edicion.title.value = f"Editar Orden N⁰ {self.orden_id}"

            self._cargar_dd_edicion()
            # Añadir y abrir el diálogo de edición
            e.page.overlay.append(self.dialogo_edicion)
            self.dialogo_edicion.open = True
            e.page.update()

        else:
            # Manejar el caso en que no se pudo cargar la orden
            print(
                f"Error: No se pudo cargar la orden con ID {self.orden_id} para editar."
            )

    def _guardar_cambios(self, e):
        cliente_id_actualizado = self._edit_dd_cliente.value
        servicio_id_actualizado = self._edit_dd_servicio.value
        vehiculo_actualizado = self._edit_txt_vehiculo.value.strip()
        descripcion_actualizado = self._edit_txt_descripcion.value.strip()
        estado_actualizado = self._edit_txt_estado.value.strip()

        if (
                not cliente_id_actualizado
                or not servicio_id_actualizado
                or not vehiculo_actualizado
                or not descripcion_actualizado
                or not estado_actualizado
        ):
            return
        orden_actualizada = self.manejo_orden.editar_orden(
            self.orden_id,
            cliente=cliente_id_actualizado,
            servicio=servicio_id_actualizado,
            vehiculo=vehiculo_actualizado,
            descripcion=descripcion_actualizado,
            estado=estado_actualizado,
        )

        if orden_actualizada:
            print("Orden actualizada")
            self.cliente = orden_actualizada.get("cliente_nombre", "")
            self.servicio = orden_actualizada.get("servicio_nombre", "")
            self.vehiculo = orden_actualizada.get("vehiculo", "")
            self.descripcion = orden_actualizada.get("descripcion", "")
            self.fecha_orden = orden_actualizada.get("fecha_orden", "")
            self.estado = orden_actualizada.get("estado", "")

            self._txt_servicio_card.value = self.servicio
            self._txt_cliente_card.value = self.cliente
            self._txt_vehiculo_card.value = self.vehiculo
            self._txt_descripcion_card.value = self.descripcion
            self._txt_fecha_orden_card.value = self.fecha_orden
            self._txt_estado_card.value = self.estado

            self._txt_dialog_vehiculo_title.value = (
                f"Orden N⁰ {self.orden_id}:    {self.vehiculo}"
            )
            self._txt_dialog_servicio_value.value = self.servicio
            self._txt_dialog_cliente_value.value = self.cliente
            self._txt_dialog_descripcion_value.value = self.descripcion
            self._txt_dialog_fecha_orden_value.value = self.fecha_orden
            self._txt_dialog_estado_value.value = self.estado

            self.update()
            self.close_dialogo(e)

    def eliminar_orden(self, e):
        try:
            orden_eliminada = self.manejo_orden.eliminar_orden(self.orden_id)

            if orden_eliminada:
                print(f"Orden eliminada id: {self.orden_id}")
                if self in container_ordenes_ui.grid.controls:
                    container_ordenes_ui.grid.controls.remove(self)
                    container_ordenes_ui.grid.update()
                else:
                    print(f"Contenedor de id {self.orden_id} no esta en el grid")

            self.close_dialogo(e)
        except Exception as e:
            print(e)

    def close_dialogo(self, e):
        """Cierra el dialogo modal"""
        # """Cierra el diálogo modal."""
        e.page.overlay[-1].open = False
        e.page.update()
        e.page.overlay.pop()


class AgregarOrden(ft.Container):
    def __init__(self):
        super().__init__(
            padding=30,
            border_radius=15,
            animate_scale=ft.Animation(200, ft.AnimationCurve.EASE_IN_CIRC),
            on_hover=self._on_hover,
            on_click=self.abrir_dialogo,
            bgcolor=ft.Colors.GREY_900,
        )

        self.manejo_servicios = ManejoServicio()
        self.manejo_ordenes = ManejoOrdenes()
        self.manejo_clientes = ManejoCliente()

        # -------CAMPOS DE TEXTO-------
        self.dd_servicio = ft.Dropdown(
            label="Servicio",
            enable_filter=True,
            editable=True,
            options=[],
            col=6,
            width=200,
        )
        self.dd_cliente = ft.Dropdown(
            label="Cliente",
            enable_filter=True,
            editable=True,
            options=[],
            col=6,
            width=200,
        )
        self.txt_mecanico = ft.TextField(label="Mecanico", col=6)

        self.txt_vehiculo = ft.TextField(
            label="Vehiculo",
        )
        self.txt_descripcion = ft.TextField(
            label="Descripción",
            multiline=True,
            max_lines=7,
        )
        self.txt_estado = ft.TextField(label="Estado", col=6)

        # -------BOTONES-------
        self.btn_registrar = ft.ElevatedButton("Registrar", on_click=self.agregar_orden)
        self.btn_cancelar = ft.ElevatedButton(
            "Cancelar", on_click=lambda e: self.close_dialogo(e)
        )

        # -------Dialogo-------
        self.dialogo = ft.AlertDialog(
            modal=True,
            title=ft.Text("Orden de Servicio"),
            content=ft.Container(  # El container se adaptará a la altura limitada
                width=400,  # Puedes darle un ancho fijo al contenido si quieres
                content=ft.Column(
                    [
                        ft.Row([self.dd_servicio, self.dd_cliente]),
                        self.txt_vehiculo,
                        self.txt_descripcion,
                        self.txt_estado,
                    ],
                    spacing=15,  # Añadir algo de espacio entre campos
                ),
            ),
            actions=[self.btn_registrar, self.btn_cancelar],
            actions_alignment=ft.MainAxisAlignment.END,  # Alinear botones
        )

        self.content = ft.Container(
            content=ft.Icon(
                ft.Icons.ADD_BOX_ROUNDED,
                size=72,
                color=ft.Colors.with_opacity(0.8, "blue"),
            ),
            bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.GREY_800),
            border_radius=15,
        )

    def _on_hover(self, e):
        container = e.control
        hover = e.data == "true"

        if hover:
            container.scale = 1.1
            container.elevation = 20
        else:
            container.scale = 1
            container.elevation = 2

        container.update()

    def close_dialogo(self, e):
        """Cierra el dialogo modal"""
        # """Cierra el diálogo modal."""
        e.page.overlay[-1].open = False
        e.page.update()
        e.page.overlay.pop()

    def abrir_dialogo(self, e):
        e.control.page.overlay.append(self.dialogo)
        self.dialogo.open = True
        e.control.page.update()
        self.cargar_dds()

    def cargar_dds(self):
        clientes = self.manejo_clientes.cargar_clientes()
        servicios = self.manejo_servicios.cargar_servicios()

        # DD SERVICIOS
        self.dd_servicio.options = [
            ft.dropdown.Option(
                text=servicio.get("descripcion", ""), key=str(servicio.get("id", ""))
            )
            for servicio in servicios
        ]
        self.dd_servicio.update()

        # DD CLIENTES
        self.dd_cliente.options = [
            ft.dropdown.Option(
                key=cliente.get("id", ""), text=cliente.get("nombre", "")
            )
            for cliente in clientes
        ]
        self.dd_cliente.update()

    def agregar_orden(self, e):
        orden_guardada = self.manejo_ordenes.guardar_orden(
            cliente=self.dd_cliente.value.strip(),
            servicio=self.dd_servicio.value.strip(),
            vehiculo=self.txt_vehiculo.value.strip(),
            descripcion=self.txt_descripcion.value.strip(),
            estado=self.txt_estado.value.strip(),
        )
        if orden_guardada:
            orden = OrdenContainer(
                orden_id=orden_guardada.get("id", ""),
                cliente=orden_guardada.get(
                    "cliente_nombre", ""
                ),  # O el nombre del cliente si lo devuelves
                servicio=orden_guardada.get(
                    "servicio_nombre", ""
                ),  # O la descripción del servicio si la devuelves
                vehiculo=orden_guardada.get(
                    "vehiculo", ""
                ),  # Viene directamente de la API
                descripcion=orden_guardada.get("descripcion", ""),  # Viene de la API
                fecha_orden=orden_guardada.get(
                    "fecha_orden", ""
                ),  # <--- ¡Obtén la fecha del API!
                estado=orden_guardada.get("estado", ""),
            )
            container_ordenes_ui.grid.controls.insert(1, orden)
            self.txt_estado.value = ""
            self.txt_vehiculo.value = ""
            self.txt_descripcion.value = ""
            self.txt_estado.update()
            self.txt_descripcion.update()
            self.txt_vehiculo.update()

        e.page.overlay[-1].open = False
        e.page.update()
        e.page.overlay.pop()
        container_ordenes_ui.grid.update()


add_container = AgregarOrden()

manejo_orden = ManejoOrdenes()


def cargar_orden(e):
    ordenes = manejo_orden.cargar_ordenes()
    ordenes.reverse()
    for datos in ordenes:
        orden = OrdenContainer(
            datos.get("id", ""),
            datos.get("cliente_nombre", ""),
            datos.get("servicio_nombre", ""),
            datos.get("vehiculo", ""),
            datos.get("descripcion", ""),
            datos.get("fecha_orden", ""),
            datos.get("estado", ""),
        )
        container_ordenes_ui.grid.controls.append(orden)
        container_ordenes_ui.grid.update()


# region VISTA
class OrdenesUi(ft.Container):
    def __init__(self):
        super().__init__(expand=True, padding=5)

        self.grid = ft.GridView(
            controls=[
                add_container,
            ],
            expand=True,
            max_extent=300,
            spacing=16.5,
            run_spacing=16.5,
        )

        self.content = ft.Column(
            controls=[
                ft.Text(
                    "Ordenes de Trabajo", theme_style=ft.TextThemeStyle.TITLE_LARGE
                ),
                ft.Container(content=self.grid, padding=15, expand=True),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        )


container_ordenes_ui = OrdenesUi()
