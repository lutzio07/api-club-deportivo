from flask import Blueprint, jsonify, request
from ..services import deportes as deportes_service

deportes_bp = Blueprint('deportes', __name__)

# --- FUNCIONES DE ERRORES ---
# Aca deberian ir las funciones para los codigos de error

# --- RUTAS ---

@deportes_bp.route('/deportes', methods=['GET'])
def get_deportes():
    # Rechaza query params desconocidos
    if request.args:
        return jsonify({"error": "Parámetros no permitidos"}), 400
    deportes = deportes_service.listar_deportes()
    return jsonify({"deportes": deportes}), 200