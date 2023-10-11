import re
from datetime import datetime
from dateutil import parser
from decimal import Decimal
import subprocess
import fitz

def extraer_informacion_desde_texto(texto):

    monto_total = None
    numero_factura = None
    fecha_emision = None

    numero_factura_match = re.search(r"FACTURA ELECTRONICA\nNº(\d+)", texto)
    if numero_factura_match:
        numero_factura = numero_factura_match.group(1)
    
    # Patrón para buscar la fecha de emisión

    fecha_emision_match = re.search(r"Fecha Emision: (.+)", texto)
    if fecha_emision_match:
        fecha_emision_str = fecha_emision_match.group(1)
        # Intentar analizar la fecha utilizando dateutil.parser
        try:
            fecha_emision = parser.parse(fecha_emision_str, fuzzy=True)
        except Exception as e:
            # Manejar el caso de fecha inválida, por ejemplo, imprimir un mensaje de error
            print(f"Error al analizar la fecha: {str(e)}")
            fecha_emision = None

        # Verificar si la fecha es válida (por ejemplo, si el día es mayor a 31)
        if fecha_emision:
            if fecha_emision.day > 31:
                # Tratar como un posible error tipográfico y asignar None a la fecha
                fecha_emision = None
    

    monto_total_match = re.search(r"TOTAL \$([\d.,]+)", texto)
    if monto_total_match:
        monto_total_str = monto_total_match.group(1)
        # Reemplazar ',' por '' y convertir a Decimal
        monto_total = Decimal(monto_total_str.replace(',', ''))

    # Variables para almacenar la información extraída
    informacion = {
        'numero_factura': numero_factura,
        'fecha_emision': fecha_emision,
        'monto_total': monto_total,
        'nombre_cliente': '',
        'rut_cliente': '',
        'direccion_cliente': '',
        # Otros campos de interés
    }

    # Realizar búsqueda de patrones en el texto para extraer información
    if re.search(r'SEÑOR\(ES\): (.+)', texto):
        informacion['nombre_cliente'] = re.search(r'SEÑOR\(ES\): (.+)', texto).group(1)
    rut_cliente_match = re.search(r'R.U.T.: (.+)', texto)
    if rut_cliente_match:
        rut_cliente = rut_cliente_match.group(1)
        # Formatear el RUT (eliminar puntos y agregar guion)
        rut_cliente = re.sub(r'\.', '', rut_cliente)
        rut_cliente = re.sub(r'[^0-9kK]', '', rut_cliente)
        rut_cliente = f"{rut_cliente[:-1]}-{rut_cliente[-1]}"
        informacion['rut_cliente'] = rut_cliente
    if re.search(r'DIRECCION: (.+)', texto):
        informacion['direccion_cliente'] = re.search(r'DIRECCION: (.+)', texto).group(1)
    if re.search(r'TOTAL \$([\d.,]+)', texto):
        informacion['monto_total'] = float(re.search(r'TOTAL \$([\d.,]+)', texto).group(1).replace(',', '.'))

    return informacion


def extraer_detalles_cargas_gas(texto_completo):
    # Inicializar una lista para almacenar la información de las cargas de gas
    cargas_gas = []

    # Buscar todas las coincidencias de detalles de carga de gas licuado
    matches = re.finditer(r'- (.*?) (\d+)K (\d+) (\d+,\d+) (\d+,\d+)', texto_completo)

    for match in matches:
        # Extraer los detalles y guardarlos en un diccionario
        detalle = {
            'descripcion': match.group(1),
            'cantidad': int(match.group(2)),
            'precio_unitario': Decimal(match.group(4).replace(',', '')),
            'total': Decimal(match.group(5).replace(',', ''))
        }
        cargas_gas.append(detalle)

    return cargas_gas


