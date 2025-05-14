import requests
import json

from config import API_BASE_URL


class ManejoServicio:
    """Clase para manejar los servicios de la base de datos"""

    def __init__(self):

        self.api_url = f"{API_BASE_URL}servicio/"

    def cargar_servicios(self):
        """Carga los servicios desde la base de datos"""
        try:
            try:
                response = requests.get(self.api_url)
                response.raise_for_status()
            except requests.ConnectionError:
                print("Error de conexión: No se pudo conectar al servidor.")
                return []
            except requests.HTTPError as http_err:
                print(f"Error HTTP: {http_err}")
                return []
            return response.json()
        except Exception as e:
            print(f"Error al cargar los servicios: {e}")
            return []

    def guardar_servicio(self, descripcion, precio):
        """Guarda un servicio en la base de datos"""
        datos_servicio = {"descripcion": descripcion, "precio": precio}
        try:
            response = requests.post(self.api_url, json=datos_servicio)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.ConnectionError:
            print("Error de conexión: No se pudo conectar a la API de servicios.")
            return None

        except requests.exceptions.Timeout:
            print("Tiempo de espera agotado al guardar el servicio en la API.")
            return None

        except requests.exceptions.HTTPError as http_err:
            print(f"Error HTTP al guardar el servicio: {http_err}")
            try:

                error_details = http_err.response.json()
                print("--- Detalles del error de validación de la API ---")
                print(json.dumps(error_details, indent=2))
                print("-------------------------------------------------")

            except json.JSONDecodeError:
                print("La respuesta de error HTTP no contiene JSON válido.")
                print(
                    f"Cuerpo de respuesta raw: {http_err.response.text}"
                )  # Muestra el texto raw si no es JSON

            return None

        except requests.exceptions.RequestException as req_err:
            # Captura otros posibles errores de requests
            print(f"Otro error de red/API al guardar el servicio: {req_err}")
            return None

        except Exception as e:
            print(f"Error al guardar el servicio: {e}")
            return None

    def eliminar_servicio(self, servicio_id):
        """Elimina un servicio en la base de datos"""
        try:
            response = requests.delete(f"{self.api_url + servicio_id}/")
            response.raise_for_status()
            return True
        except Exception as e:
            print(f"Error al eliminar el cliente: {e}")

    def editar_servicio(self, servicio_id, descripcion, precio):
        """Edita un servicio en la base de datos"""
        datos_servicio = {"descripcion": descripcion, "precio": precio}
        try:
            response = requests.put(
                f"{self.api_url + servicio_id}/", json=datos_servicio
            )
            response.raise_for_status()
            print(f"Servicio editado exitosamente {response.json()}")
            return response.json()
        except Exception as e:
            print(f"Error al editar el cliente: {e}")
            return None
