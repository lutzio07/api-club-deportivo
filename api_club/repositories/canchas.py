from api_club.db import obtener_conexion


def obtener_todas(limit, offset, nombre=None, id_deporte=None, techada=None, activa=None):
    conexion = obtener_conexion()

    cursor = conexion.cursor(dictionary=True)

    consulta = """
        SELECT
            id,
            nombre,
            id_deporte,
            precio_hora,
            techada,
            activa
        FROM canchas
    """

    condiciones = []
    parametros = []

    if nombre is not None:
        condiciones.append("LOWER(nombre) LIKE LOWER(%s)")
        parametros.append(f"%{nombre}%")

    if id_deporte is not None:
        condiciones.append("id_deporte = %s")
        parametros.append(id_deporte)

    if techada is not None:
        condiciones.append("techada = %s")
        parametros.append(techada)

    if activa is not None:
        condiciones.append("activa = %s")
        parametros.append(activa)

    if condiciones:
        consulta += " WHERE " + " AND ".join(condiciones)

    consulta += " ORDER BY id ASC LIMIT %s OFFSET %s"

    parametros.extend([limit, offset])

    cursor.execute(consulta, parametros)

    canchas = cursor.fetchall()

    cursor.close()
    conexion.close()

    return canchas


def contar_canchas(nombre=None, id_deporte=None, techada=None, activa=None):
    conexion = obtener_conexion()

    cursor = conexion.cursor()

    consulta = "SELECT COUNT(*) FROM canchas"

    condiciones = []
    parametros = []

    if nombre is not None:
        condiciones.append("LOWER(nombre) LIKE LOWER(%s)")
        parametros.append(f"%{nombre}%")

    if id_deporte is not None:
        condiciones.append("id_deporte = %s")
        parametros.append(id_deporte)

    if techada is not None:
        condiciones.append("techada = %s")
        parametros.append(techada)

    if activa is not None:
        condiciones.append("activa = %s")
        parametros.append(activa)

    if condiciones:
        consulta += " WHERE " + " AND ".join(condiciones)

    cursor.execute(consulta, parametros)

    total = cursor.fetchone()[0]

    cursor.close()
    conexion.close()

    return total


def crear_cancha(nombre, id_deporte, precio_hora, techada, activa):
    conexion = obtener_conexion()

    cursor = conexion.cursor()

    consulta = """
        INSERT INTO canchas (
            nombre,
            id_deporte,
            precio_hora,
            techada,
            activa
        )
        VALUES (%s, %s, %s, %s, %s)
    """

    cursor.execute(consulta, (
        nombre,
        id_deporte,
        precio_hora,
        techada,
        activa
    ))

    conexion.commit()

    id_nueva = cursor.lastrowid

    cursor.close()
    conexion.close()

    return id_nueva

def existe_deporte(id_deporte):
    conexion = obtener_conexion()

    cursor = conexion.cursor()

    consulta = """
        SELECT 1
        FROM deportes
        WHERE id = %s
    """

    cursor.execute(consulta, (id_deporte,))

    resultado = cursor.fetchone()

    cursor.close()
    conexion.close()

    return resultado is not None
