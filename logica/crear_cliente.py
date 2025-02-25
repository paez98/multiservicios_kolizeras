from client_supabase import supabase
# from faker import Faker


def guardar_cliente(nombre, telefono, direccion):
    """Guarda un nuevo cliente en la base de datos."""
    try:
        response = (
            supabase.table("clientes")
            .insert({"nombre": nombre, "telefono": telefono, "direccion": direccion})
            .execute()
        )
        print(f"Cliente registrado {response}")
    except Exception as e:
        print(f"Error al resgistrar el cliente{e}")
