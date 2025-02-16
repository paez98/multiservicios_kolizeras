from client_supabase import supabase


def editar_cliente(cliente_id, nombre, telefono, direccion):
    """Edita un cliente en Supabase."""
    try:
        supabase.table("clientes").update(
            {"nombre": nombre, "telefono": telefono, "direccion": direccion}
        ).eq("id", cliente_id).execute()
        print("Cliente actualizado correctamente")
    except Exception as e:
        print(f"Error al actualizar el cliente: {e}")


# from models.cliente import Cliente
# def editar_cliente(cliente_id, nombre, telefono, direccion):
#     """Edita un cliente en la base de datos."""
#     try:
#         cliente = Cliente.buscar_por_id(cliente_id)
#         if cliente:
#             cliente.nombre = nombre
#             cliente.telefono = telefono
#             cliente.direccion = direccion
#             cliente.actualizar()
#             print("Cliente actualizado exitosamente.")
#         else:
#             print('Cliente no encontrado')
#     except Exception as e:
#         print(f"Error al actualizar cliente: {e}")
