from http.client import responses
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

    def cargar_orden_id(self, orden_id):
        try:
            response = requests.get(f"{self.api_url}{orden_id}/")
            response.raise_for_status()
            return response.json()

        except requests.exceptions.HTTPError as http_err:
            print(f"Error HTTP al cargar orden {orden_id}: {http_err}")
            if http_err.response is not None:
                try:
                    print(f"Detalle del error HTTP: {http_err.response.json()}")
                except:
                    pass  # Ignorar si no es JSON
            return None  # Indica fallo o no encontrada

        except requests.exceptions.RequestException as req_err:
            print(
                f"Error de conexión o solicitud al cargar orden {orden_id}: {req_err}"
            )
            return None  # Indica fallo
        except Exception as e:
            print(f"Ocurrió un error inesperado al cargar orden {orden_id}: {e}")
            return None

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

    def eliminar_orden(self, orden_id):
        try:
            response = requests.delete(f"{self.api_url}{orden_id}/")
            response.raise_for_status()
            return True
        except requests.exceptions.HTTPError as http_err:
            print(http_err)
            return http_err

    def editar_orden(self, orden_id, cliente, servicio, vehiculo, descripcion, estado):
        datos_actualizados = {
            "cliente": cliente,
            "servicio": servicio,
            "vehiculo": vehiculo,
            "descripcion": descripcion,
            "estado": estado,
        }

        try:
            response = requests.put(
                f"{self.api_url}{orden_id}/", json=datos_actualizados
            )
            response.raise_for_status()
            print(f"Orden {orden_id} actualizada: {response.json()}")
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            print(f"Error HTTP al editar orden {orden_id}: {http_err}")
            if http_err.response is not None:
                try:
                    print(f"Detalle del error HTTP: {http_err.response.json()}")
                except:
                    pass  # Ignorar si no es JSON
            return None  # Indica fallo

        except requests.exceptions.RequestException as req_err:
            print(
                f"Error de conexión o solicitud al editar orden {orden_id}: {req_err}"
            )
            return None  # Indica fallo de conexión/solicitud

        except Exception as e:
            print(f"Ocurrió un error inesperado al editar orden {orden_id}: {e}")
            return None  # Indica otro tipo de fallo
