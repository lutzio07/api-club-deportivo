from datetime import datetime

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

def validar_datos_actualizacion_cancha(datos):

    if not isinstance(datos, dict):
        return "El cuerpo debe ser un objeto JSON"

    campos_permitidos = {
        "nombre",
        "precio_hora",
        "techada",
        "activa"
    }

    campos_recibidos = set(datos.keys())

    campos_desconocidos = campos_recibidos - campos_permitidos

    if campos_desconocidos:
        return f"Campo(s) desconocido(s): {', '.join(campos_desconocidos)}"

    if not datos:
        return "Debe indicar al menos un campo para actualizar"

    if "nombre" in datos:

        if not isinstance(datos["nombre"], str):
            return "nombre debe ser un texto"

        if not datos["nombre"].strip():
            return "nombre no puede estar vacío"

    if "precio_hora" in datos:

        if not isinstance(datos["precio_hora"], int) or isinstance(datos["precio_hora"], bool):
            return "precio_hora debe ser un número entero"

        if datos["precio_hora"] <= 0:
            return "precio_hora debe ser mayor que 0"

    if "techada" in datos:

        if not isinstance(datos["techada"], bool):
            return "techada debe ser true o false"

    if "activa" in datos:

        if not isinstance(datos["activa"], bool):
            return "activa debe ser true o false"

    return None

def validar_parametros_disponibilidad(fecha, hora_inicio, hora_fin):

    if not fecha:
        return "El parámetro fecha es obligatorio"

    if not hora_inicio:
        return "El parámetro hora_inicio es obligatorio"

    if not hora_fin:
        return "El parámetro hora_fin es obligatorio"

    try:
        datetime.strptime(fecha, "%Y-%m-%d")
    except ValueError:
        return "fecha debe tener el formato AAAA-MM-DD"

    try:
        hora_inicio_obj = datetime.strptime(hora_inicio, "%H:%M:%S")
    except ValueError:
        return "hora_inicio debe tener el formato HH:00:00"

    try:
        hora_fin_obj = datetime.strptime(hora_fin, "%H:%M:%S")
    except ValueError:
        return "hora_fin debe tener el formato HH:00:00"

    if hora_inicio_obj.minute != 0 or hora_inicio_obj.second != 0:
        return "hora_inicio debe ser una hora exacta"

    if hora_fin_obj.minute != 0 or hora_fin_obj.second != 0:
        return "hora_fin debe ser una hora exacta"

    if hora_inicio_obj >= hora_fin_obj:
        return "hora_inicio debe ser menor que hora_fin"

    if hora_inicio_obj.hour < 8:
        return "La hora de inicio debe ser a partir de las 08:00:00"

    if hora_fin_obj.hour > 23:
        return "La hora de fin no puede superar las 23:00:00"

    return None

def validar_filtros_disponibilidad(id_deporte=None, techada=None):

    if id_deporte is not None:

        if not isinstance(id_deporte, int) or isinstance(id_deporte, bool):
            return "id_deporte debe ser un número entero"

        if id_deporte < 1:
            return "id_deporte debe ser un número positivo"

    if techada is not None:

        if not isinstance(techada, bool):
            return "techada debe ser true o false"

    return None

def validar_paginacion(limit=None, offset=None):

    if limit is not None:

        if not isinstance(limit, int) or isinstance(limit, bool):
            return "_limit debe ser un número entero"

        if limit < 1 or limit > 100:
            return "_limit debe estar entre 1 y 100"

    if offset is not None:

        if not isinstance(offset, int) or isinstance(offset, bool):
            return "_offset debe ser un número entero"

        if offset < 0:
            return "_offset no puede ser negativo"

    return None