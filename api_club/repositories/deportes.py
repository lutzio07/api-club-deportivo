from api_club.db import obtener_conexion

def obtener_todos():
    conexion = obtener_conexion()
    cursor = None
    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT id, nombre FROM deportes")
        deportes = cursor.fetchall()
        return deportes
    finally:
        if cursor:
            cursor.close()
        conexion.close()