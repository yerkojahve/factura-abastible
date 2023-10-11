import mysql.connector


config = {
    "host": "localhost",
    "user": "root",
    "password": "YERKOf11badgcs3",
    "database": "factura"
}

connection = mysql.connector.connect(**config)


def guardar_datos_en_db(datos,idcliente):
    try:
        cursor = connection.cursor()

        # Obtener los datos del diccionario
        numero_factura = datos['numero_factura']
        fecha_emision = datos['fecha_emision']
        monto_total = datos['monto_total']
        nombre_cliente = datos['nombre_cliente']
        rut_cliente = datos['rut_cliente']
        direccion_cliente = datos['direccion_cliente']

        # Consulta SQL para insertar los datos en la tabla factura
        query_insertar_factura = "INSERT INTO factura (numero_factura, fecha, monto, nombre_cliente, rut_comercio, direccion, idcliente) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        valores = (numero_factura, fecha_emision, monto_total, nombre_cliente, rut_cliente, direccion_cliente, idcliente)

        cursor.execute(query_insertar_factura, valores)
        connection.commit()

        cursor.close()
        print("Datos guardados en la base de datos correctamente.")
    except mysql.connector.Error as err:
        print(f"Error al guardar los datos en la base de datos: {err}")

def eliminar_factura_por_numero(numero_factura):
    try:
        cursor = connection.cursor()
        
        # Consulta SQL para eliminar una factura por número de factura
        query_eliminar_factura = "DELETE FROM factura WHERE numero_factura = %s"
        valores = (numero_factura,)

        cursor.execute(query_eliminar_factura, valores)
        connection.commit()

        cursor.close()
        print(f"Factura con número {numero_factura} eliminada correctamente.")
    except mysql.connector.Error as err:
        print(f"Error al eliminar la factura: {err}")

def actualizar_datos_en_db(id_factura, nuevos_datos):
    try:
        cursor = connection.cursor()
        
        # Consulta SQL para actualizar los datos en la tabla factura
        query_actualizar_factura = "UPDATE factura SET numero_factura = %s, fecha = %s, monto = %s, nombre_cliente = %s, rut_comercio = %s, direccion = %s WHERE id = %s"
        valores = (nuevos_datos['numero_factura'], nuevos_datos['fecha_emision'], nuevos_datos['monto_total'], nuevos_datos['nombre_cliente'], nuevos_datos['rut_cliente'], nuevos_datos['direccion_cliente'], id_factura)

        cursor.execute(query_actualizar_factura, valores)
        connection.commit()

        cursor.close()
        print("Datos actualizados en la base de datos correctamente.")
    except mysql.connector.Error as err:
        print(f"Error al actualizar los datos en la base de datos: {err}")


def obtener_rut_comercio_por_cliente(nombre_cliente):
    try:
        cursor = connection.cursor()
        query = "SELECT RUT FROM cliente WHERE Nombre = %s"
        cursor.execute(query, (nombre_cliente,))
        resultado = cursor.fetchone()
        cursor.close()

        if resultado:
            return resultado[0]  # Devolver el RUT si se encuentra el cliente
        else:
            return None  # Devolver None si el cliente no se encuentra
    except mysql.connector.Error as err:
        print(f"Error al obtener el RUT del cliente: {err}")
        return None

def obtener_id_cliente(rut):
        try:
            cursor = connection.cursor()
            query = "SELECT idCliente FROM cliente WHERE Rut = %s"
            cursor.execute(query, (rut,))
            resultado = cursor.fetchone()
            cursor.close()
            if resultado:
                return resultado[0]  # Devuelve el idCliente si se encontró el Rut
            else:
                return None  # Retorna None si no se encontró el Rut
        except mysql.connector.Error as err:
            print(f"Error al obtener el idCliente: {err}")
            return None
        
def buscar_cliente_por_id(id_cliente):
    try:
        cursor = connection.cursor()
        query = """
            SELECT c.Nombre, c.Rut, f.direccion, c.Telefono, f.numero_factura, f.Fecha, f.monto
            FROM cliente c
            LEFT JOIN factura f ON c.idCliente = f.idCliente
            WHERE c.idCliente = %s
        """
        cursor.execute(query, (id_cliente,))
        resultado = cursor.fetchone()
        cursor.close()

        if resultado:
            nombre, rut_cliente, direccion_factura, telefono, num_factura, fecha, monto = resultado
            cliente = {
                "Nombre": nombre,
                "Rut": rut_cliente,
                "Direccion Factura": direccion_factura,
                "Telefono": telefono,
                "Factura": {
                    "NumeroFactura": num_factura,
                    "Fecha": fecha,
                    "Monto": monto
                }
            }
            return cliente  # Devuelve un diccionario con los datos del cliente y su factura
        else:
            return None  # Retorna None si no se encontró el cliente con el id
    except mysql.connector.Error as err:
        print(f"Error al buscar el cliente por id: {err}")
        return None



