import re

PATRON_EMAIL = re.compile(r'^[^@\s]+@[^@\s]+\.[^@\s]+$')


def validar_datos_socios(limit, offset, nombre, activo):
    if limit < 1 or limit > 100:
        raise ValueError("El parámetro limit debe estar entre 1 y 100 exclusivamente.")

    if offset < 0:
        raise ValueError("El parámetro offset debe ser mayor o igual que 0.")

    if activo is not None and not isinstance(activo, bool):
        raise ValueError("El parámetro activo debe ser true o false")


def validar_alta_socio(datos):
    """
    Valida el cuerpo de POST /socios.
    Devuelve un dict con nombre y email ya limpios (nombre sin espacios
    en los extremos, email en minúsculas y sin espacios).
    """
    if not isinstance(datos, dict):
        raise ValueError("El cuerpo debe ser un objeto JSON")

    campos_permitidos = {"nombre", "email"}
    campos_desconocidos = set(datos.keys()) - campos_permitidos
    if campos_desconocidos:
        raise ValueError(f"Campo(s) desconocido(s): {', '.join(campos_desconocidos)}")

    campos_faltantes = campos_permitidos - set(datos.keys())
    if campos_faltantes:
        raise ValueError(f"Falta(n) campo(s) obligatorio(s): {', '.join(campos_faltantes)}")

    nombre = datos["nombre"]
    email = datos["email"]

    if not isinstance(nombre, str) or not nombre.strip():
        raise ValueError("El nombre no puede estar vacío")

    if not isinstance(email, str) or not PATRON_EMAIL.match(email.strip()):
        raise ValueError("El email no tiene un formato válido")

    return {
        "nombre": nombre.strip(),
        "email": email.strip().lower(),
    }


def validar_actualizacion_socio(datos):
    """
    Valida el cuerpo de PATCH /socios/{id}.
    Devuelve un dict solo con los campos que vinieron, ya limpios/tipados.
    """
    if not isinstance(datos, dict) or not datos:
        raise ValueError("El cuerpo no puede estar vacío")

    campos_permitidos = {"nombre", "email", "activo"}
    campos_desconocidos = set(datos.keys()) - campos_permitidos
    if campos_desconocidos:
        raise ValueError(f"Campo(s) desconocido(s): {', '.join(campos_desconocidos)}")

    campos_validados = {}

    if "nombre" in datos:
        nombre = datos["nombre"]
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre no puede estar vacío")
        campos_validados["nombre"] = nombre.strip()

    if "email" in datos:
        email = datos["email"]
        if not isinstance(email, str) or not PATRON_EMAIL.match(email.strip()):
            raise ValueError("El email no tiene un formato válido")
        campos_validados["email"] = email.strip().lower()

    if "activo" in datos:
        activo = datos["activo"]
        if not isinstance(activo, bool):
            raise ValueError("El campo activo debe ser true o false")
        campos_validados["activo"] = activo

    return campos_validados