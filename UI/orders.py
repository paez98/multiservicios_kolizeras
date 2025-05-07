import flet as ft
from logica.manejo_servicio import ManejoServicio
from logica.manejo_ordenes import ManejoOrdenes
from ui.home import container_ordenes_home


class OrdenContainer(ft.Container):
    def __init__(self, servicio, vehiculo: str, descripcion, fecha_limite):
        super().__init__(
            border_radius=15,
            on_hover=self._on_hover,
            on_click=self.abrir_dialogo,
            animate_scale=ft.Animation(200, ft.AnimationCurve.EASE_IN_CIRC),
        )
        self.servicio = servicio
        self.vehiculo = vehiculo
        self.descripcion = descripcion
        self.fecha_limite = fecha_limite

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
                        # Fecha de entrega
                        ft.Text(self.fecha_limite, text_align=ft.TextAlign.RIGHT),
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
            title=ft.Text(f"Detalles Orden: {self.vehiculo.capitalize()}"),
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
                        ft.Text(self.fecha_limite),
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

        # -------CAMPOS DE TEXTO-------
        self.dd_servicio = ft.Dropdown(
            label="Servicio", enable_filter=True, editable=True, options=[]
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
        self.txt_fecha = ft.TextField(label="Fecha de entrega", col=6)

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
                        self.dd_servicio,
                        self.txt_vehiculo,
                        self.txt_descripcion,
                        self.txt_fecha,
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
        self.cargar_dropdown()

    # -----Metodos-----
    def cargar_dropdown(self):
        servicios = self.manejo_servicios.cargar_servicios()
        self.dd_servicio.options = [
            ft.dropdown.Option(text=servicio["descripcion"]) for servicio in servicios
        ]

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

    def agregar_orden(self, e):
        self.manejo_ordenes.guardar_orden(
            servicio=self.dd_servicio.value.strip(),
            vehiculo=self.txt_vehiculo.value.strip(),
            descripcion=self.txt_descripcion.value.strip(),
            fecha=self.txt_fecha.value.strip(),
        )
        orden = OrdenContainer(
            servicio=self.dd_servicio.value.capitalize(),
            vehiculo=self.txt_vehiculo.value.capitalize(),
            descripcion=self.txt_descripcion.value.capitalize(),
            fecha_limite=self.txt_fecha.value.capitalize(),
        )

        container_ordenes_ui.grid.controls.insert(1, orden)
        e.page.overlay[-1].open = False
        e.page.update()
        e.page.overlay.pop()
        container_ordenes_ui.grid.update()
        print("asdasdasd")

        container_ordenes_home.actualizar_tabla(
            self.dd_servicio.value,
            self.txt_fecha.value,
            "parao",
        )

    # def cargar_ordenes(self):
    #     ordenes = self.manejo_ordenes.cargar_ordenes()
    #     ordenes.reverse()
    #     for datos in ordenes:
    #         orden = OrdenContainer(
    #             datos["servicio"],
    #             datos["vehiculo"],
    #             datos["descripcion"],
    #             datos["fecha"],
    #         )
    #         container_ordenes_ui.grid.controls.append(orden)
    #
    #     container_ordenes_ui.grid.update()


add_container = AgregarOrden()

manejo_orden = ManejoOrdenes()


def cargar_orden(e):
    ordenes = manejo_orden.cargar_ordenes()
    ordenes.reverse()
    for datos in ordenes:
        orden = OrdenContainer(
            datos["servicio"],
            datos["vehiculo"],
            datos["descripcion"],
            datos["fecha"],
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
