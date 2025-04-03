from client_supabase import supabase


class ManejoServicio:
    """Clase para manejar los servicios de la base de datos"""

    def __init__(self):
        self.table_name = "servicios"
        self.db_client = supabase

    def cargar_servicios(self):
        """Carga los servicios desde la base de datos"""
        try:
            response = (
                self.db_client.table(self.table_name)
                .select("*")
                .order("id", desc=False)
                .execute()
            )
            return response.data
        except Exception as e:
            print(f"Error al cargar los servicios: {e}")
            return []

    def guardar_servicio(self, descripcion, precio):
        """Guarda un cliente en la base de datos"""
        try:
            response = (
                supabase.table(self.table_name)
                .insert({"descripcion": descripcion, "precio": precio})
                .execute()
            )
            print(f"Servicio guardado exitosamente {response}")
            return response.data
        except Exception as e:
            print(f"Error al guardar el servicio: {e}")
            return None

    def eliminar_servicio(self, servicio_id):
        """Elimina un servicio en la base de datos"""
        try:
            response = (
                supabase.table(self.table_name).delete().eq("id", servicio_id).execute()
            )
            print(f"Cliente eliminado exitosamente {response}")
            return response.data
        except Exception as e:
            print(f"Error al eliminar el cliente: {e}")

    def editar_servicio(self, servicio_id, descripcion, precio):
        """Edita un cliente en la base de datos"""
        try:
            response = (
                supabase.table(self.table_name)
                .update(
                    {"descripcion": descripcion, "precio": precio},
                    returning="representation",
                )
                .eq("id", servicio_id)
                .execute()
            )
            print(f"Cliente editado exitosamente {response.data}")
            return response.data
        except Exception as e:
            print(f"Error al editar el cliente: {e}")
            return None
