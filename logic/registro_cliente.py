from conection import Database

db = Database()


def cargar_clientes():
    """Carga los clientes desde la base de datos."""
    try:
        clientes = db.fetch_all(
            "SELECT id, nombre, telefono, direccion FROM cliente")
        return clientes
    except Exception as e:
        print(f"Error al cargar clientes: {e}")
        return []


def guardar_cliente(nombre, contacto, direccion):
    """Guarda un nuevo cliente en la base de datos."""
    try:
        db.execute(
            "INSERT INTO cliente (nombre, telefono, direccion) VALUES (%s, %s, %s)",
            (nombre, contacto, direccion)
        )
        print("Cliente registrado exitosamente.")
    except Exception as e:
        print(f"Error al registrar cliente: {e}")


def eliminar_cliente(cliente_id):
    """Elimina un cliente de la base de datos."""
    try:
        db.execute("DELETE FROM cliente WHERE id = %s", (cliente_id,))
        print("Cliente eliminado exitosamente.")
    except Exception as e:
        print(f"Error al eliminar cliente: {e}")


def editar_cliente(cliente_id, nombre, contacto, direccion):
    """Edita un cliente en la base de datos."""
    try:
        db.execute(
            "UPDATE cliente SET nombre = %s, telefono = %s, direccion = %s WHERE id = %s",
            (nombre, contacto, direccion, cliente_id)
        )
        print("Cliente actualizado exitosamente.")
    except Exception as e:
        print(f"Error al actualizar cliente: {e}")
