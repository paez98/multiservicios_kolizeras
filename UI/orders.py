import flet as ft
from typing import Optional
from logica.manejo_servicio import ManejoServicio
from logica.manejo_ordenes import ManejoOrdenes
from logica.manejo_cliente import ManejoCliente
from ui.home import container_ordenes_home


class OrdenContainer(ft.Container):
    def __init__(
        self,
        cliente,
        servicio,
        vehiculo: str,
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
        self.cliente = cliente
        self.servicio = servicio
        self.vehiculo = vehiculo
        self.descripcion = descripcion
        self.fecha_orden = fecha_orden
        self.estado = estado

        self.base_content = ft.Card(
            elevation=5,
            content=ft.Container(
                content=ft.Column(
                    [
                        # Servicio a realizar
                        ft.Text(
                            self.servicio,
                            theme_style=ft.TextThemeStyle.TITLE_LARGE,
                            weight=ft.FontWeight.BOLD,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.Text(
                            self.cliente,
                            theme_style=ft.TextThemeStyle.TITLE_MEDIUM,
                            weight=ft.FontWeight.BOLD,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        # Vehiculo
                        ft.Text(
                            self.vehiculo, theme_style=ft.TextThemeStyle.TITLE_MEDIUM
                        ),
                        ft.Text(
                            self.descripcion,
                            overflow=ft.TextOverflow.ELLIPSIS,
                            max_lines=5,
                            no_wrap=True,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.Text(self.fecha_orden),
                        # Estado
                        ft.Text(self.estado, text_align=ft.TextAlign.RIGHT),
                    ],
                    spacing=5,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=15,
            ),
        )

        self.content = self.base_content
        # -----DIALOGO MODAL-----
        self.detalles_dialogo = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"Detalles Orden: {self.vehiculo}"),
            content=ft.Container(
                width=400,
                padding=10,
                content=ft.Column(
                    [
                        # Sección Servicio
                        ft.Row(
                            [
                                ft.Icon(ft.Icons.MISCELLANEOUS_SERVICES),
                                ft.Text("Servicio:", weight=ft.FontWeight.BOLD),
                            ]
                        ),
                        ft.Text(self.servicio),
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
                            content=ft.Text(self.descripcion),
                            padding=ft.padding.only(left=5),
                        ),
                        ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                        # Sección Fecha Límite
                        ft.Row(
                            [
                                ft.Icon(ft.Icons.EVENT_AVAILABLE),
                                ft.Text("Fecha Límite:", weight=ft.FontWeight.BOLD),
                            ]
                        ),
                        ft.Text(self.estado),
                    ],
                    spacing=5,
                    scroll=ft.ScrollMode.ADAPTIVE,
                    height=300,
                ),
            ),
            actions=[ft.TextButton("Cerrar", on_click=self.close_dialogo)],
            actions_alignment=ft.MainAxisAlignment.END,
        )

    # -----METODOS-----
    def _on_hover(self, e):
        container = e.control
        hover = e.data == "true"
        container.scale = 1.1 if hover else 1.0
        container.elevation = 20 if hover else 5  # Ajustar elevación con hover
        container.update()

    def abrir_dialogo(self, e):
        e.control.page.overlay.append(self.detalles_dialogo)
        self.detalles_dialogo.open = True
        e.control.page.update()

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
