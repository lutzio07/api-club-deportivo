from datetime import datetime

def validar_filtros_reservas(id_cancha=None, id_socio=None, estado=None, fecha_desde=None, fecha_hasta=None):
    
    if id_cancha is not None:
        try:
            id_cancha_int = int(id_cancha)
            if id_cancha_int < 1:
                return "id_cancha debe ser un número positivo"
        except ValueError:
            return "id_cancha debe ser un número entero"

    if id_socio is not None:
        try:
            id_socio_int = int(id_socio)
            if id_socio_int < 1:
                return "id_socio debe ser un número positivo"
        except ValueError:
            return "id_socio debe ser un número entero"

    estados_permitidos = ["confirmada", "cancelada", "finalizada"]
    if estado is not None:
        if estado not in estados_permitidos:
            return f"estado debe ser uno de los siguientes: {', '.join(estados_permitidos)}"

    fecha_desde_obj = None
    if fecha_desde is not None:
        try:
            fecha_desde_obj = datetime.strptime(fecha_desde, "%Y-%m-%d")
        except ValueError:
            return "fecha_desde debe tener el formato AAAA-MM-DD"
        
    fecha_hasta_obj = None
    if fecha_hasta is not None:
        try:
            fecha_hasta_obj = datetime.strptime(fecha_hasta, "%Y-%m-%d")
        except ValueError:
            return "fecha_hasta debe tener el formato AAAA-MM-DD"

    if fecha_desde_obj and fecha_hasta_obj:
        if fecha_desde_obj > fecha_hasta_obj:
            return "fecha_desde debe ser menor o igual a fecha_hasta"

    return None

def validar_paginacion(limit=None, offset=None):
    if limit is not None:
        try:
            limit_int = int(limit)
            if limit_int < 1 or limit_int > 100:
                return "_limit debe estar entre 1 y 100"
        except ValueError:
            return "_limit debe ser un número entero"

    if offset is not None:
        try:
            offset_int = int(offset)
            if offset_int < 0:
                return "_offset no puede ser negativo"
        except ValueError:
            return "_offset debe ser un número entero"

    return None