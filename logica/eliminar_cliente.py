from models.cliente import Cliente


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
