from models.cliente import Cliente

cliente = Cliente()


def cargar_clientes():
    """Carga los clientes desde la base de datos."""
    try:
        clientes = Cliente.cargar_todos()
        return [
            {
                "id": c.id,
                "nombre": c.nombre,
                "telefono": c.telefono,
                "direccion": c.direccion,
            }
            for c in clientes
        ]
    except Exception as e:
        print(f"Error al cargar los clientes: {e}")
        return []
