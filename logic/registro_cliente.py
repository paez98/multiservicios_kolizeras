from models.cliente import Cliente

cliente = Cliente()


def cargar_clientes():
    """Carga los clientes desde la base de datos."""
    try:
        clientes = Cliente.cargar_todos()
        return [{'id': c.id, 'nombre': c.nombre, 'telefono': c.telefono, 'direccion': c.direccion} for c in clientes]
    except Exception as e:
        print(f"Error al cargar los clientes: {e}")
        return []


def guardar_cliente(nombre, telefono, direccion):
    """Guarda un nuevo cliente en la base de datos."""
    try:
        nuevo_cliente = Cliente(
            nombre=nombre, telefono=telefono, direccion=direccion)
        nuevo_cliente.guardar()
        print("Cliente registrado exitosamente.")
    except Exception as e:
        print(f"Error al registrar cliente: {e}")


def eliminar_cliente(cliente_id):
    """Elimina un cliente de la base de datos."""
    try:
        cliente = Cliente.buscar_por_id(cliente_id)
        if cliente:
            cliente.eliminar()
            print("Cliente eliminado exitosamente.")
        else:
            print('Cliente no encontrado')
    except Exception as e:
        print(f"Error al eliminar cliente: {e}")


def editar_cliente(cliente_id, nombre, telefono, direccion):
    """Edita un cliente en la base de datos."""
    try:
        cliente = Cliente.buscar_por_id(cliente_id)
        if cliente:
            cliente.nombre = nombre
            cliente.telefono = telefono
            cliente.direccion = direccion
            cliente.actualizar()
            print("Cliente actualizado exitosamente.")
        else:
            print('Cliente no encontrado')
    except Exception as e:
        print(f"Error al actualizar cliente: {e}")
