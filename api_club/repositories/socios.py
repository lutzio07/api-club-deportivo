from api_club.db import obtener_conexion
def get_socios(limit, offset, nombre=None, activo=None):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    query = "SELECT * FROM socios WHERE 1=1"
    params = []
    if nombre:
        query += " AND nombre LIKE %s"
        params.append(f"%{nombre}")
    if activo is not None:  
        query += (" AND activo = %s")
        params.append(activo)
    query += (" ORDER BY id LIMIT %s OFFSET %s")
    params.append(limit)
    params.append(offset)
    cursor.execute(query, params)
    socios = cursor.fetchall()
    cursor.close()  
    conexion.close()
    return socios   