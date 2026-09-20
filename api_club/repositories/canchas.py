from api_club.db import obtener_conexion


def obtener_todas():
    conexion = obtener_conexion()

    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            id,
            nombre,
            id_deporte,
            precio_hora,
            techada,
            activa
        FROM canchas
        ORDER BY id ASC
    """)

    canchas = cursor.fetchall()

    cursor.close()
    conexion.close()

    return canchas