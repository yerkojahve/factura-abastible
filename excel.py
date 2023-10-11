import pandas as pd
import mysql.connector

# Conectar a la base de datos MySQL
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="YERKOf11badgcs3",
    database="factura"
)

# Leer el archivo Excel
excel_file = "../LISTADO CLIENTES.xlsx"  # Reemplaza con la ruta de tu archivo Excel

df = pd.read_excel(excel_file)

# Iterar sobre las filas del DataFrame
for index, row in df.iterrows():
    rut = row['Rut Comercio']  # Supongo que 'Rut' es la columna del rut en tu Excel
    nombre = row['N FANTASIA']  # Supongo que 'Nombre' es la columna del nombre en tu Excel
    telefono = row['N TELEFONO']  # Supongo que 'N TELEFONO' es la columna del teléfono en tu Excel

    if pd.notna(rut) and pd.notna(nombre) and pd.notna(telefono):
        # Actualizar el teléfono en la tabla 'cliente' basado en el Rut y el Nombre
        cursor = connection.cursor()
        query = "UPDATE cliente SET Telefono = %s WHERE Rut = %s AND Nombre = %s"
        values = (telefono, rut, nombre)

        try:
            cursor.execute(query, values)
            connection.commit()
            cursor.close()
            print(f"Teléfono {telefono} actualizado para Rut: {rut}")
        except mysql.connector.IntegrityError as e:
            print(f"Error al actualizar el teléfono {telefono} para Rut: {rut} - {str(e)}")
            # Continuar con la siguiente fila en caso de error
            continue
    else:
        # Datos faltantes en la fila, omitir esta iteración
        continue

# Cerrar la conexión a la base de datos
connection.close()




""""
# Iterar sobre las filas del DataFrame
for index, row in df.iterrows():
    idCliente = row['IDCLIENTE']  # Asegúrate de que coincida con el nombre de la columna en tu Excel
    rut_comercio = row['RUT_COMERCIO']
    direccion = row['DIRECCION']
    nombre_cliente = row['NOMBRE_CLIENTE']
    Fecha = row['FECHA']
    monto = row['MONTO']
    numero_factura = row['NUMERO_FACTURA']

    # Realizar la inserción en la tabla 'factura'
    cursor = connection.cursor()
    query = "INSERT INTO factura (idCliente, rut_comercio, direccion, nombre_cliente, Fecha, monto, numero_factura) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    values = (idCliente, rut_comercio, direccion, nombre_cliente, Fecha, monto, numero_factura)
    cursor.execute(query, values)
    connection.commit()
    cursor.close()

# Cerrar la conexión a la base de datos
connection.close() """