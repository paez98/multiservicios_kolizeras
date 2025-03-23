import flet as ft
from typing import Optional


def crear_campo_texto(label, hint_text: Optional[str] = None):
    "Crea un campo de texto estilizado"
    return ft.TextField(
        label=label,
        width=300,
        border_color="#2196f3",
        hint_text=hint_text,
        border="underline",
    )


def crear_boton(text, icon, on_click, color):
    "Creamos un boton estilizado"
    return ft.ElevatedButton(
        text=text,
        icon=icon,
        width=150,
        style=ft.ButtonStyle(color=color),
        on_click=on_click,
        disabled=True,
    )


def manejar_seleccion(e):
    # Obtener la fila seleccionada
    fila_seleccionada = e.control  # Esto devuelve la instancia de DataRow seleccionada

    # Alternar el estado de selección
    fila_seleccionada.selected = not fila_seleccionada.selected
    fila_seleccionada.update()  # Actualizar la fila en la interfaz

    if fila_seleccionada.selected:  # Verificar si la fila está seleccionada
        # Acceder al contenido de la primera celda (ID)
        id_seleccionado = fila_seleccionada.cells[0].content.value
        print(f"El ID es: {id_seleccionado}")
    else:
        print("Fila deseleccionada")
