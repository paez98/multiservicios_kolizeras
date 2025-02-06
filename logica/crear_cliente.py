from models.cliente import Cliente

cliente = Cliente()


def guardar_cliente(nombre, telefono, direccion):
    """Guarda un nuevo cliente en la base de datos."""
    try:
        nuevo_cliente = Cliente(
            nombre=nombre, telefono=telefono, direccion=direccion)
        nuevo_cliente.guardar()
        print("Cliente registrado exitosamente.")
    except Exception as e:
        print(f"Error al registrar cliente: {e}")
