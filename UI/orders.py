import flet as ft
from logica.manejo_servicio import ManejoServicio


class OrdenContainer(ft.Container):
    def __init__(self, servicio, vehiculo, descripcion, fecha_limite):
        super().__init__(
            border=ft.border.all(1, "red"),
            border_radius=15,
            on_hover=self._on_hover,
            on_click=self._on_click,
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
                        ft.Text(self.servicio),
                        # Vehiculo
                        ft.Text(self.vehiculo),
                        ft.Text(self.descripcion),
                        # Fecha de entrega
                        ft.Text(self.fecha_limite),
                    ],
                    spacing=5,
                ),
                padding=15,
            ),
        )

        self.content = self.base_content

    def _on_hover(self, e):
        container = e.control
        hover = e.data == "true"
        container.scale = 1.1 if hover else 1.0
        container.elevation = 20 if hover else 5  # Ajustar elevación con hover
        container.update()

    def _on_click(self, e):
        print("alao")


class AgregarOrden(ft.Container):
    def __init__(self):
        super().__init__(
            border=ft.border.all(1, "red"),
            padding=30,
            border_radius=15,
            animate_scale=ft.Animation(200, ft.AnimationCurve.EASE_IN_CIRC),
            on_hover=self._on_hover,
            on_click=self.abrir_dialogo,
        )
        self.manejo_servicios = ManejoServicio()

        # -------CAMPOS DE TEXTO-------
        self.dd_servicio = ft.Dropdown(
            label="Servicio", enable_filter=True, editable=True, options=[]
        )

        self.txt_vehiculo = ft.TextField(
            label="Vehiculo",
        )
        self.txt_descripcion = ft.TextField(
            label="Descripción",
            multiline=True,
            max_lines=7,
        )
        self.txt_fecha = ft.TextField(label="Fecha de entrega")

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
            # bgcolor=ft.Colors.with_opacity(0.9, ft.Colors.GREY_400),
        )

        self.content = ft.Container(
            content=ft.Icon(
                ft.Icons.ADD_BOX_ROUNDED,
                size=72,
                color=ft.Colors.with_opacity(0.8, "blue"),
            ),
            border=ft.border.all(1, "blue"),
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
        orden = OrdenContainer(
            servicio=self.dd_servicio.value.capitalize(),
            vehiculo=self.txt_vehiculo.value.capitalize(),
            descripcion=self.txt_descripcion.value.capitalize(),
            fecha_limite=self.txt_fecha.value.capitalize(),
        )
        container_ordenes.grid.controls.append(orden)
        e.page.overlay[-1].open = False
        e.page.update()
        e.page.overlay.pop()
        container_ordenes.grid.update()
        print("asdasdasd")


add_container = AgregarOrden()


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
                ft.Container(content=self.grid, padding=15),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )


container_ordenes = OrdenesUi()
