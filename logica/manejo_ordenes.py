import requests
from config import API_BASE_URL
from client_supabase import supabase


class ManejoOrdenes:
    def __init__(self):
        self.api_url = f"{API_BASE_URL}orden/"

    def cargar_ordenes(self):
        try:
            try:
                response = requests.get(f"{API_BASE_URL}orden")
                response.raise_for_status()
            except requests.ConnectionError:
                print("Error de conexción: No se puedo conectar al sevidor")
                return []
            except requests.HTTPError as htto_err:
                print(f"Error HTTP:{htto_err}")
                return []
            return response.json()
        except Exception as e:
            print(f"Error al cargar los pagos: {e}")

    def guardar_orden(self, cliente, servicio, vehiculo, descripcion, estado):
        datos_orden = {
            "cliente": cliente,
            "servicio": servicio,
            "vehiculo": vehiculo,
            "descripcion": descripcion,
            "estado": estado,
        }

        try:
            response = requests.post(self.api_url, json=datos_orden)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            print(f"Error al guardar {http_err}")
            print(f"detalle de error, {http_err.response.json()}")
            return

        except Exception as e:
            print(f"Error al crear la orden{e}")
            return None
