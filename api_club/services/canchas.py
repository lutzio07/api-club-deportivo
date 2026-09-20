from api_club.repositories import canchas as canchas_repo


def listar_canchas():
    return canchas_repo.obtener_todas()