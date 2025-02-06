from database import Conexion


class Cliente:
    def __init__(self, id=None, nombre=None, telefono=None, direccion=None):
        """
        Constructor de la clase Cliente.
        :param id: ID del cliente (opcional, autoincremental en la base de datos).
        :param nombre: Nombre del cliente.
        :param telefono: Teléfono del cliente.
        :param direccion: Dirección del cliente.
        """
        self.id = id
        self.nombre = nombre
        self.telefono = telefono
        self.direccion = direccion
        self.db = Conexion()

    def guardar(self):
        '''Guarda el cliente en la base de datos'''
        try:
            query = "INSERT INTO cliente(nombre, telefono, direccion) VALUES (%s, %s, %s)"
            self.db.execute(
                query, (self.nombre, self.telefono, self.direccion))
            print('Cliente registrado exitoso')
        except Exception as e:
            print(f"Error al registrar cliente: {e}")

    def eliminar(self):
        'Elimina al cliente en id'
        if not self.id:
            print('No se puede eliminar un ciente sin id')
            return
        try:
            query = "DELETE FROM cliente WHERE id = %s"
            self.db.execute(query, (self.id))
            print('Cliente eliminado exitoso')
        except Exception as e:
            print(f'Error al eliminar el cliente: {e}')

    def actualizar(self):
        'Actualiza los datos del cliente en la base de datos'
        if not self.id:
            print('No se puede acutualizar un cliente sin ID')
            return
        try:
            query = "UPDATE cliente SET nombre = %s, telefono = %s, direccion = %s WHERE id = %s"
            self.db.execute(
                query, (self.nombre, self.telefono, self.direccion))
            print('Cliente actualizado exitoso')
        except Exception as e:
            print(f'Error al actualizar el cliente: {e}')

    @staticmethod
    def cargar_todos():
        '''
          Carga todos los clientes desde la base de datos.
          :return: Lista de instancias de Cliente.
        '''
        db = Conexion()
        try:
            query = "SELECT cliente_id, nombre, telefono, direccion FROM cliente"
            resultados = db.fetch_all(query)
            clientes = []
            for row in resultados:
                cliente = Cliente(
                    id=row[0], nombre=row[1], telefono=row[2], direccion=row[3])
                clientes.append(cliente)
            return clientes

        except Exception as e:
            print(f"Error al cargar clientes: {e}")

    @staticmethod
    def buscar_por_id(cliente_id):
        """
        Busca un cliente por su ID.
        :param cliente_id: ID del cliente a buscar.
        :return: Instancia de Cliente si se encuentra, None si no existe.
        """
        db = Conexion()
        try:
            query = 'SELECT cliente_id, nombre, telefono, direccion FROM cliente WHERE id = %s'
            resultado = db.fetch_all(query, (cliente_id))
            if resultado:
                row = resultado[0]
                return Cliente(id=row[0], nombre=row[1], telefono=row[2], direccion=row[3])
            return None
        except Exception as e:
            print(f'Error al buscar cliente por ID: {e}')
            return None
