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


def obtener_por_id(id_socio):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM socios WHERE id = %s", (id_socio,))
    socio = cursor.fetchone()
    cursor.close()
    conexion.close()
    return socio


def existe_email(email, excluir_id=None):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    query = "SELECT 1 FROM socios WHERE email = %s"
    params = [email]
    if excluir_id is not None:
        query += " AND id != %s"
        params.append(excluir_id)
    query += " LIMIT 1"
    cursor.execute(query, params)
    resultado = cursor.fetchone()
    cursor.close()
    conexion.close()
    return resultado is not None


def crear_socio(nombre, email):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(
        "INSERT INTO socios (nombre, email, activo) VALUES (%s, %s, TRUE)",
        (nombre, email)
    )
    conexion.commit()
    id_nuevo = cursor.lastrowid
    cursor.close()
    conexion.close()
    return id_nuevo


def actualizar_socio(id_socio, campos):
    """
    campos: dict con las columnas a actualizar (nombre/email/activo).
    Arma el UPDATE dinámicamente según qué campos vinieron.
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    columnas = ", ".join(f"{campo} = %s" for campo in campos)
    valores = list(campos.values())
    valores.append(id_socio)
    cursor.execute(f"UPDATE socios SET {columnas} WHERE id = %s", valores)
    conexion.commit()
    cursor.close()
    conexion.close()