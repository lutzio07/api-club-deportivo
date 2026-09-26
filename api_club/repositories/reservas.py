from api_club.db import obtener_conexion

def obtener_todas(limit, offset, id_cancha=None, id_socio=None, estado=None, fecha_desde=None, fecha_hasta=None):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    consulta = """
        SELECT
            id,
            id_cancha,
            id_socio,
            fecha_hora_inicio,
            fecha_hora_fin,
            estado,
            precio_hora,
            precio_total
        FROM reservas
    """

    condiciones = []
    parametros = []

    if id_cancha is not None:
        condiciones.append("id_cancha = %s")
        parametros.append(id_cancha)
    if id_socio is not None:
        condiciones.append("id_socio = %s")
        parametros.append(id_socio)
    if estado is not None:
        condiciones.append("estado = %s")
        parametros.append(estado)
    if fecha_desde is not None:
        condiciones.append("DATE(fecha_hora_inicio) >= %s")
        parametros.append(fecha_desde)
    if fecha_hasta is not None:
        condiciones.append("DATE(fecha_hora_inicio) <= %s")
        parametros.append(fecha_hasta)

    if condiciones:
        consulta += " WHERE " + " AND ".join(condiciones)

    consulta += " ORDER BY id ASC LIMIT %s OFFSET %s"
    parametros.extend([limit, offset])

    cursor.execute(consulta, parametros)
    reservas = cursor.fetchall()
    cursor.close()
    conexion.close()

    return reservas

def contar_reservas(id_cancha=None, id_socio=None, estado=None, fecha_desde=None, fecha_hasta=None):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    consulta = "SELECT COUNT(*) FROM reservas"
    
    condiciones = []
    parametros = []

    if id_cancha is not None:
        condiciones.append("id_cancha = %s")
        parametros.append(id_cancha)
    if id_socio is not None:
        condiciones.append("id_socio = %s")
        parametros.append(id_socio)
    if estado is not None:
        condiciones.append("estado = %s")
        parametros.append(estado)
    if fecha_desde is not None:
        condiciones.append("DATE(fecha_hora_inicio) >= %s")
        parametros.append(fecha_desde)
    if fecha_hasta is not None:
        condiciones.append("DATE(fecha_hora_inicio) <= %s")
        parametros.append(fecha_hasta)

    if condiciones:
        consulta += " WHERE " + " AND ".join(condiciones)

    cursor.execute(consulta, parametros)
    total = cursor.fetchone()[0]

    cursor.close()
    conexion.close()

    return total
