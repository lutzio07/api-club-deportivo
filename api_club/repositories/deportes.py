from api_club.db import obtener_conexion

def obtener_todos():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)  # dictionary=True devuelve dicts en vez de tuplas
    cursor.execute("SELECT id, nombre FROM deportes")
    deportes = cursor.fetchall()
    cursor.close()
    conexion.close()
    return deportes