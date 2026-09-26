from api_club.db import obtener_conexion

def convertir_cancha(cancha):
    if cancha is not None:
        cancha["techada"] = bool(cancha["techada"])
        cancha["activa"] = bool(cancha["activa"])
    return cancha

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

    for cancha in canchas:
        convertir_cancha(cancha)

    cursor.close()
    conexion.close()

    return canchas

def obtener_disponibles(
    fecha,
    hora_inicio,
    hora_fin,
    id_deporte=None,
    techada=None,
    limit=10,
    offset=0
):
    conexion = obtener_conexion()

    cursor = conexion.cursor(dictionary=True)

    consulta = """
        SELECT
            c.id,
            c.nombre,
            c.id_deporte,
            c.precio_hora,
            c.techada,
            c.activa
        FROM canchas c
        WHERE c.activa = TRUE
    """

    condiciones = []
    parametros = []

    if id_deporte is not None:
        condiciones.append("c.id_deporte = %s")
        parametros.append(id_deporte)

    if techada is not None:
        condiciones.append("c.techada = %s")
        parametros.append(techada)

    condiciones.append("""
        NOT EXISTS (
            SELECT 1
            FROM reservas r
            WHERE r.id_cancha = c.id
              AND r.estado = 'confirmada'
              AND r.fecha_hora_inicio < CONCAT(%s, ' ', %s)
              AND r.fecha_hora_fin > CONCAT(%s, ' ', %s)
        )
    """)

    parametros.extend([
        fecha,
        hora_fin,
        fecha,
        hora_inicio
    ])

    consulta += " AND " + " AND ".join(condiciones)

    consulta += " ORDER BY c.id ASC LIMIT %s OFFSET %s"

    parametros.extend([limit, offset])

    cursor.execute(consulta, parametros)
    canchas_disponibles = cursor.fetchall()

    for cancha in canchas_disponibles:
        convertir_cancha(cancha)

    cursor.close()
    conexion.close()

    return canchas_disponibles

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

def contar_disponibles(
    fecha,
    hora_inicio,
    hora_fin,
    id_deporte=None,
    techada=None
):
    conexion = obtener_conexion()

    cursor = conexion.cursor()

    consulta = """
        SELECT COUNT(*)
        FROM canchas c
        WHERE c.activa = TRUE
    """

    condiciones = []
    parametros = []

    if id_deporte is not None:
        condiciones.append("c.id_deporte = %s")
        parametros.append(id_deporte)

    if techada is not None:
        condiciones.append("c.techada = %s")
        parametros.append(techada)

    condiciones.append("""
        NOT EXISTS (
            SELECT 1
            FROM reservas r
            WHERE r.id_cancha = c.id
              AND r.estado = 'confirmada'
              AND r.fecha_hora_inicio < CONCAT(%s, ' ', %s)
              AND r.fecha_hora_fin > CONCAT(%s, ' ', %s)
        )
    """)

    parametros.extend([
        fecha,
        hora_fin,
        fecha,
        hora_inicio
    ])

    consulta += " AND " + " AND ".join(condiciones)

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


def obtener_datos_cancha(id_cancha):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM canchas WHERE id = %s", (id_cancha,))
    cancha = cursor.fetchone()

    convertir_cancha(cancha)

    cursor.close()
    conexion.close()
    return cancha


def actualizar_cancha(id_cancha, datos):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    campos = []
    parametros = []

    if "nombre" in datos:
        campos.append("nombre = %s")
        parametros.append(datos["nombre"])

    if "precio_hora" in datos:
        campos.append("precio_hora = %s")
        parametros.append(datos["precio_hora"])

    if "techada" in datos:
        campos.append("techada = %s")
        parametros.append(datos["techada"])

    if "activa" in datos:
        campos.append("activa = %s")
        parametros.append(datos["activa"])

    consulta = f"""
        UPDATE canchas
        SET {', '.join(campos)}
        WHERE id = %s
    """

    parametros.append(id_cancha)

    cursor.execute(consulta, parametros)

    conexion.commit()

    cursor.close()
    conexion.close()

def eliminar_cancha(id_cancha):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        "DELETE FROM canchas WHERE id = %s",
        (id_cancha,)
    )

    conexion.commit()

    cursor.close()
    conexion.close()

def tiene_reservas(id_cancha):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM reservas WHERE id_cancha = %s",
        (id_cancha,)
    )

    cantidad = cursor.fetchone()[0]

    cursor.close()
    conexion.close()

    return cantidad > 0

