from ..repositories import socios as socios_repo
def get_socios(limit, offset, nombre, activo):
    return socios_repo.get_socios(limit, offset, nombre, activo)


def crear_socio(nombre, email):
    if socios_repo.existe_email(email):
        return None, "EMAIL_DUPLICADO"

    id_nuevo = socios_repo.crear_socio(nombre, email)
    return socios_repo.obtener_por_id(id_nuevo), None


def obtener_socio_por_id(id_socio):
    return socios_repo.obtener_por_id(id_socio)


def actualizar_socio(id_socio, campos):
    socio = socios_repo.obtener_por_id(id_socio)
    if not socio:
        return None, "NO_ENCONTRADO"

    if "email" in campos and socios_repo.existe_email(campos["email"], excluir_id=id_socio):
        return None, "EMAIL_DUPLICADO"

    socios_repo.actualizar_socio(id_socio, campos)
    return socios_repo.obtener_por_id(id_socio), None