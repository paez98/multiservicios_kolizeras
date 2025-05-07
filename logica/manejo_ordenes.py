from client_supabase import supabase


class ManejoOrdenes:
    def __init__(self):
        self.table_name = "orden"
        self.db_client = supabase

    def cargar_ordenes(self):
        try:
            response = self.db_client.table(self.table_name).select("*").execute()
            return response.data
        except Exception as e:
            print(f"Error al cargar las ordenes{e}")
            return []

    def guardar_orden(self, servicio, vehiculo, descripcion, fecha):

        try:
            response = (
                self.db_client.table(self.table_name)
                .insert(
                    {
                        "servicio": servicio,
                        "vehiculo": vehiculo,
                        "descripcion": descripcion,
                        "fecha": fecha,
                    }
                )
                .execute()
            )
            print(f"Orden creada exitoxamente {response}")
            return response.data
        except Exception as e:
            print(f"Error al crear la orden{e}")
            return None
