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

def crear_cancha(nombre,id_deporte,precio_hora,techada,activa):
    conexion = obtener_conexion()
    cursor =conexion.cursor()
    cursor.execute("""
        INSERT INTO canchas(nombre,id_deporte,precio_hora,techada,activa) VALUES (%s,%s,%s,%s,%s)
    """,(nombre,id_deporte,precio_hora,techada,activa))

    nuevo_id = cursor.lastrowid

    conexion.commit()
    
    cursor.close()
    conexion.close()
    
    return nuevo_id

def existe_deporte(id_deporte):
    conexion = obtener_conexion()
    
    cursor = conexion.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT
        id,
        nombre
        FROM deportes
        WHERE id = %s
    """,(id_deporte,))
    
    resultado_deporte_encontrado = cursor.fetchone()
    
    cursor.close()
    conexion.close()
    
    return resultado_deporte_encontrado is not None