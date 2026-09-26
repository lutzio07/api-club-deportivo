from flask import Flask
from api_club.routes.deportes import deportes_bp
from api_club.routes.canchas import canchas_bp
from api_club.routes.socios import socios_bp
from api_club.routes.reservas import reservas_bp

app = Flask(__name__)

app.register_blueprint(deportes_bp)
app.register_blueprint(canchas_bp)
app.register_blueprint(socios_bp)
app.register_blueprint(reservas_bp)

@app.route("/")
def index():
    return "Indice de la API del club deportivo"
if __name__ == '__main__':
    app.run(port=5000, debug=True)