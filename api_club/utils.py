def formatear_error(code, message, description, level="error"):
    return {
        "errors": [{
                "code": code,
                "message": message,
                "level": level,
                "description": description
            }
        ]
    }