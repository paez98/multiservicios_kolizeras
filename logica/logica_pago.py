from client_supabase import supabase


class LogicaPago:
    """Clase para manejar la lógica de los pagos"""

    def __init__(self):
        self.table_name = "pagos"
        self.db_client = supabase

    def cargar_pagos(self):
        """Carga los pagos desde la base de datos"""
        try:
            response = (
                self.db_client.table(self.table_name)
                .select("*")
                .order("id", desc=False)
                .execute()
            )
            return response.data
        except Exception as e:
            print(f"Error al cargar los pagos: {e}")
            return []

    def guardar_pago(self, nombre, servicio, monto, fecha):
        """Guarda un pago en la base de datos"""
        try:
            response = (
                supabase.table(self.table_name)
                .insert(
                    {
                        "nombre": nombre,
                        "servicio": servicio,
                        "monto": monto,
                        "fecha": fecha,
                    }
                )
                .execute()
            )

            return response.data
        except Exception as e:
            print(f"Error al guardar el pago: {e}")
            return None
