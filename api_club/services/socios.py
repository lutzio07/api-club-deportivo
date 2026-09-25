from ..repositories import socios as socios_repo
def get_socios(limit, offset, nombre, activo):
    return socios_repo.get_socios(limit, offset, nombre, activo)