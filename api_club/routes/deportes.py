from flask import Blueprint, jsonify

from ..services import deportes as deportes_service

deportes_bp = Blueprint('deportes', __name__)

# --- FUNCIONES DE ERRORES ---
# Aca deberian ir las funciones para los codigos de error

# --- RUTAS ---

@deportes_bp.route('/deportes', methods=['GET'])
def get_deportes():
    deportes = deportes_service.listar_deportes()

    if not deportes:
        return '', 204

    return jsonify({"deportes": deportes})