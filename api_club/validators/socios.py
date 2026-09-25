def validar_datos_socios(limit, offset, nombre, activo):
    if limit < 1 or limit > 100:
        raise ValueError("El parámetro limit debe estar entre 1 y 100 exclusivamente.")

    if offset < 0:
        raise ValueError("El parámetro offset debe ser mayor o igual que 0.")

    if activo is not None and activo not in ["0", "1", 0, 1]:
        raise ValueError("El parámetro activo debe ser 0 o 1 ")