# Este archivo actualmente no esta activo pero se conservaa para futuros usos
import os  # Para acceder a variables del sistema
import psycopg2  # Librería para PostgreSQL
from dotenv import load_dotenv  # Para leer el archivo .env

load_dotenv(dotenv_path=".env")  # Carga las variables del archivo .env

print(os.getenv("dbname"))  # Nombre de la base de datos
print(os.getenv("user"))  # Usuario de PostgreSQL
print(os.getenv("password"))  # Contraseña
print(os.getenv("host"))  # Dirección (localhost = tu pc)
print(os.getenv("port"))  # Puerto predeterminado = 5432


class Conexion:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname=os.getenv("dbname"),  # Nombre de la base de datos
            user=os.getenv("user"),  # Usuario de PostgreSQL
            password=os.getenv("password"),  # Contrasena
            host=os.getenv("host"),  # Direccion (localhost = tu pc)
            port=os.getenv("port"),  # Puerto predeterminado = 5432
        )
        self.cursor = self.conn.cursor()

    def execute(self, query, params=None):
        try:
            self.cursor.execute(query, params or ())  # Ejecuta la consulta SQL
            self.conn.commit()  # Guarda los cambios
        except Exception as e:
            self.conn.rollback()  # Deshace los cambios si hay error
            raise e  # Muestra el error

    def fetch_all(self, query, params=None):
        self.execute(query, params)  # Ejecuta la consulta

        return self.cursor.fetchall()  # Obtiene todos los resultados

    def close(self):
        self.cursor.close()  # Cierra el mando a distancia
        self.conn.close()  # Cierra la puerta de la casa
