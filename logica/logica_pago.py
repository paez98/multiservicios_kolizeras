import requests
import json
from config import API_BASE_URL


class LogicaPago:
    """Clase para manejar la lógica de los pagos"""

    def __init__(self):
        self.api_url = f"{API_BASE_URL}pago/"

    def cargar_pagos(self):
        """Carga los pagos desde la base de datos"""
        try:
            try:
                response = requests.get(self.api_url)
                response.raise_for_status()  # Lanza un error si la respuesta no es 200
                return response.json()
            except requests.ConnectionError:
                print("Error de conexión: No se pudo conectar al servidor.")
                return []
            except requests.HTTPError as http_err:
                print(f"Error HTTP: {http_err}")
                return []
            return response.json()
        except Exception as e:
            print(f"Error al cargar los pagos: {e}")
            return []

    def guardar_pago(self, cliente, servicio, metodo, monto, referencia, fecha_pago):
        """Guarda un pago en la base de datos"""
        data_pago = {
            "cliente": cliente,
            "servicio": servicio,
            "metodo": metodo,
            "monto": monto,
            "referencia": referencia,
            "fecha_pago": fecha_pago,
        }
        try:
            response = requests.post(self.api_url, json=data_pago)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:

            print(f"Error HTTP al guardar el pago: {http_err}")

            # El status code está en http_err.response.status_code

            if http_err.response.status_code == 400:

                print(
                    "--- Detalles del error de validación de la API (400 Bad Request) ---"
                )

                try:

                    # El cuerpo de la respuesta 400 de DRF suele contener JSON con errores de validación

                    error_details = http_err.response.json()

                    print(json.dumps(error_details, indent=2))  # Imprime el JSON bonito

                    print(
                        "---------------------------------------------------------------"
                    )

                    # Puedes retornar estos detalles si tu lógica de UI fuera a manejarlos granularmente

                except json.JSONDecodeError:

                    print("La respuesta 400 no contiene JSON válido.")

                    print(f"Cuerpo de respuesta raw: {http_err.response.text}")

            else:

                # Otros errores HTTP (ej. 404, 500)

                print(
                    f"Ocurrió un error HTTP inesperado (Status {http_err.response.status_code})."
                )

                # ... (manejar otros errores HTTP si es necesario) ...

            # Mostrar un SnackBar de error (general para HTTPError, o más específico)

            return None  # Indica fallo

        except requests.exceptions.RequestException as req_err:

            # ... (manejar otros errores de requests y retornar None) ...

            print(f"Error de Red o Solicitud: {req_err}")

            return None

        except Exception as e:

            # ... (manejar otros errores inesperados y retornar None) ...

            print(f"Error inesperado: {e}")

            return None
