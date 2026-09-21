def validar_datos_cancha(datos):

    if not isinstance(datos, dict):
        return "El cuerpo debe ser un objeto JSON"

    campos_permitidos = {
        "nombre",
        "id_deporte",
        "precio_hora",
        "techada",
        "activa"
    }

    campos_recibidos = set(datos.keys())

    campos_desconocidos = campos_recibidos - campos_permitidos

    if campos_desconocidos:
        return f"Campo(s) desconocido(s): {', '.join(campos_desconocidos)}"

    campos_obligatorios = {
        "nombre",
        "id_deporte",
        "precio_hora",
        "techada",
        "activa"
    }

    campos_faltantes = campos_obligatorios - campos_recibidos

    if campos_faltantes:
        return f"Falta(n) campo(s) obligatorio(s): {', '.join(campos_faltantes)}"

    if not isinstance(datos["nombre"], str):
        return "nombre debe ser un texto"

    if not datos["nombre"].strip():
        return "nombre no puede estar vacío"

    if not isinstance(datos["id_deporte"], int) or isinstance(datos["id_deporte"], bool):
        return "id_deporte debe ser un número entero"

    if not isinstance(datos["precio_hora"], int) or isinstance(datos["precio_hora"], bool):
        return "precio_hora debe ser un número entero"

    if not isinstance(datos["techada"], bool):
        return "techada debe ser true o false"

    if not isinstance(datos["activa"], bool):
        return "activa debe ser true o false"

    if datos["id_deporte"] < 1:
        return "id_deporte debe ser un número positivo"

    if datos["precio_hora"] <= 0:
        return "precio_hora debe ser mayor que 0"

    return None