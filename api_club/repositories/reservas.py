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

def hay_superposicion_cancha(id_cancha, fecha_hora_inicio, fecha_hora_fin):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    consulta = """
        SELECT COUNT(*) FROM reservas
        WHERE id_cancha = %s
          AND estado = 'confirmada'
          AND fecha_hora_inicio < %s
          AND fecha_hora_fin > %s
    """

    cursor.execute(consulta, (id_cancha, fecha_hora_fin, fecha_hora_inicio))
    cantidad = cursor.fetchone()[0]
    cursor.close()
    conexion.close()

    return cantidad > 0

def hay_superposicion_socio(id_socio, fecha_hora_inicio, fecha_hora_fin):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    consulta = """
        SELECT COUNT(*) FROM reservas
        WHERE id_socio = %s
          AND estado = 'confirmada'
          AND fecha_hora_inicio < %s
          AND fecha_hora_fin > %s
    """

    cursor.execute(consulta, (id_socio, fecha_hora_fin, fecha_hora_inicio))
    cantidad = cursor.fetchone()[0]
    cursor.close()
    conexion.close()

    return cantidad > 0

def crear_reserva(id_socio, id_cancha, fecha_hora_inicio, fecha_hora_fin, precio_hora, precio_total):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    consulta = """
        INSERT INTO reservas (
            id_socio, id_cancha, fecha_hora_inicio, fecha_hora_fin,
            precio_hora, precio_total, estado
        ) VALUES (%s, %s, %s, %s, %s, %s, 'confirmada')
    """
    cursor.execute(consulta, (
        id_socio, id_cancha, fecha_hora_inicio, fecha_hora_fin,
        precio_hora, precio_total
    ))

    conexion.commit()
    id_nueva = cursor.lastrowid
    cursor.close()
    conexion.close()

    return id_nueva

def obtener_reserva_por_id(id_reserva):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM reservas WHERE id = %s", (id_reserva,))
    reserva = cursor.fetchone()
    cursor.close()
    conexion.close()
    return reserva