import flet as ft


def crear_campo_texto(label, hint_text):
    'Crea un campo de texto estilizado'
    return ft.TextField(
        label=label,
        width=300,
        border_color='#2196f3',
        hint_text=hint_text
    )


def crear_boton(text, icon, on_click,  color):
    'Creamos un boton estilizado'
    return ft.ElevatedButton(
        text=text,
        icon=icon,
        width=150,
        height=50,
        style=ft.ButtonStyle(color=color),
        on_click=on_click
    )


def actualizar_tabla():
    """Actualiza la tabla de clientes."""
    # Aquí puedes agregar la lógica para actualizar la tabla
    print("Tabla actualizada")
