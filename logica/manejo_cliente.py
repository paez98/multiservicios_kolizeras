import json
import requests
from config import API_BASE_URL


class ManejoCliente:
    def __init__(self):
        self.api_url = f"{API_BASE_URL}cliente/"
        self.table_name = "alo"

    def cargar_clientes(self):
        """Carga los clientes desde la base de datos"""
        try:
            response = requests.get(self.api_url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error de red/API al cargar clientes: {e}")
            return []  # Devuelve lista vacía en error
        except json.JSONDecodeError as e:
            print(f"Error al decodificar JSON de clientes: {e}")
            return []

    def guardar_cliente(self, nombre: str, telefono: str, direccion: str):

        datos_cliente = {
            "nombre": nombre,
            "telefono": telefono,
            "direccion": direccion,
        }

        try:
            print(
                f"Intentando guardar POST a URL: {self.api_url} con datos: {datos_cliente}"
            )

            response = requests.post(self.api_url, json=datos_cliente)
            response.raise_for_status()
            print("Cliente guardado exitosamente (lógica API).")
            return response.json()  # Retorna los datos del cliente creado

        # --- CAPTURA ESPECÍFICA para errores HTTP (incluyendo 400) ---
        except requests.exceptions.HTTPError as http_err:
            print(f"Error HTTP al guardar cliente (lógica API): {http_err}")

            if http_err.response.status_code == 400:
                # Es un error 400 Bad Request: Probablemente validación.
                try:
                    # Intenta parsear el cuerpo de la respuesta 400 como JSON
                    error_details = http_err.response.json()
                    print("HTTP 400 Detalles (lógica API):", error_details)
                    # Retorna un diccionario específico para indicar error de validación
                    return {"errors": error_details}
                except json.JSONDecodeError:
                    print("HTTP 400 response body is not valid JSON (lógica API).")
                    # Retorna un diccionario de error genérico si el JSON 400 es inválido
                    return {
                        "errors": {
                            "non_field_errors": [
                                "Respuesta de error de validación inválida."
                            ]
                        }
                    }
            else:
                # Es otro error HTTP (404, 500, etc. - no 400)
                print(
                    f"Otro Error HTTP ({http_err.response.status_code}) al guardar (lógica API)."
                )
                return None  # Retorna None para otros errores HTTP

        # --- CAPTURA para otros errores de 'requests' (red, timeout, etc.) ---
        except requests.exceptions.RequestException as req_err:
            print(f"Error de Red o Solicitud (lógica API): {req_err}")
            return None  # Retorna None para errores de red/solicitud

        # --- CAPTURA para cualquier otro error inesperado ---
        except Exception as e:
            print(f"Error inesperado al guardar cliente (lógica API): {e}")
            return None  # Retorna None para errores inesperados

    def editar_cliente(self, cliente_id, nombre, telefono, direccion):
        """Edita un cliente en la base de datos"""
        datos_cliente = {"nombre": nombre, "telefono": telefono, "direccion": direccion}
        try:
            response = requests.put(f"{self.api_url + cliente_id}/", json=datos_cliente)
            response.raise_for_status()
            print(f"Cliente {cliente_id} editado exitosamente")
            return response.json()

        except requests.exceptions.HTTPError as http_error:
            print(f"Error al editar el cliente{http_error}")

            if http_error.response.status_code == 400:
                try:
                    # Intenta parsear el cuerpo de la respuesta 400 como JSON
                    error_details = http_error.response.json()
                    print("HTTP 400 Detalles (lógica API):", error_details)
                    # Retorna un diccionario específico para indicar error de validación
                    return {"errors": error_details}
                except json.JSONDecodeError:
                    print("HTTP 400 response body is not valid JSON (lógica API).")
                    # Retorna un diccionario de error genérico si el JSON 400 es inválido
                    return {
                        "errors": {
                            "non_field_errors": [
                                "Respuesta de error de validación inválida."
                            ]
                        }
                    }
            else:
                # Es otro error HTTP (404, 500, etc. - no 400)
                print(
                    f"Otro Error HTTP ({http_error.response.status_code}) al guardar (lógica API)."
                )
                return None

        except Exception as e:
            print(f"Error al editar el cliente: {e}")
            return None

    def eliminar_cliente(self, cliente_id):
        """Elimina un cliente en la base de datos"""
        try:
            response = requests.delete(f"{self.api_url + cliente_id}/")
            response.raise_for_status()
            print(f"Cliente {cliente_id} eliminado exitosamente")
            return True
        except Exception as e:
            print(f"Error al eliminar el cliente: {e}")
            return e
