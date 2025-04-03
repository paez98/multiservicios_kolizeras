from client_supabase import supabase


class ManejoCliente:
    def __init__(self):
        self.table_name = "clientes"
        self.db_client = supabase

    def cargar_clientes(self):
        """Carga los clientes desde la base de datos"""
        try:
            response = (
                self.db_client.table(self.table_name)
                .select("*")
                .order("id", desc=False)
                .execute()
            )
            return response.data
        except Exception as e:
            print(f"Error al cargar los clientes{e}")
            return []

    def cargar_nombre_clientes(self):
        """Carga los clientes desde la base de datos"""
        try:
            response = (
                supabase.table(self.table_name)
                .select("nombre")
                .order("id", desc=False)
                .execute()
            )
            return response.data
        except Exception as e:
            print(f"Error al cargar los clientes{e}")
            return []

    def guardar_cliente(self, nombre, telefono, direccion):
        """Guarda un cliente en la base de datos"""
        try:
            response = (
                supabase.table(self.table_name)
                .insert(
                    {"nombre": nombre, "telefono": telefono, "direccion": direccion}
                )
                .execute()
            )
            print(f"Cliente guardado exitosamente {response}")
            return response.data
        except Exception as e:
            print(f"Error al guardar el cliente: {e}")
            return None

    def editar_cliente(self, cliente_id, nombre, telefono, direccion):
        """Edita un cliente en la base de datos"""
        try:
            response = (
                supabase.table(self.table_name)
                .update(
                    {"nombre": nombre, "telefono": telefono, "direccion": direccion},
                    returning="representation",
                )
                .eq("id", cliente_id)
                .execute()
            )
            print(f"Cliente editado exitosamente {response.data}")
            return response.data
        except Exception as e:
            print(f"Error al editar el cliente: {e}")
            return None

    def eliminar_cliente(self, cliente_id):
        """Elimina un cliente en la base de datos"""
        try:
            response = (
                supabase.table(self.table_name).delete().eq("id", cliente_id).execute()
            )
            print(f"Cliente eliminado exitosamente {response}")
            return response.data
        except Exception as e:
            print(f"Error al eliminar el cliente: {e}")
