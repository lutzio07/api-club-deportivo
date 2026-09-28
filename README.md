## API REST - Club Deportivo 

API REST desarrollada en Python con Flask y MySQL para la gestión de reservas de canchas, deportes y socios de un club deportivo.

-
# -Integrantes del equipo-
* Lucio Villagra
* Joako Transillo
* Jorge Felix Garcia
* Eliel Castillo
* 
* Matias Ezequiel Montiel

--
# -Tecnologías utilizadas-

* Lenguaje: Python 3.x
* Framework web: Flask
* CORS: Flask-CORS
* Base de datos: MySQL 8.0
* Conector de base de datos: mysql-connector-python
* Variables de entorno: python-dotenv
* Documentación: OpenAPI 3.0 / Swagger

---
-Estructura del proyecto-

Organizamos el proyecto en capas para separar la lógica de negocio, las rutas y las consultas a la base de datos:

*api_club/*: Código principal del backend.
  * *repositories/*: Consultas SQL y acceso a MySQL.
  * *routes/*: Endpoints y manejo de peticiones HTTP.
  * *services/*: Lógica de negocio de la aplicación.
  * *validators/*: Validaciones de datos de entrada.
  * *config.py*: Configuración de la aplicación.
  * *constants.py*: Constantes globales del proyecto.
  * *db.py*: Manejo de la conexión a la base de datos.
  * *exceptions.py*: Excepciones y manejo de errores personalizados.
  * *utils.py*: Funciones auxiliares y helpers.
 *db/*:
  * *init_db.sql*: Script para crear la estructura de tablas y cargar datos iniciales.
 *docs/*:
  * *swagger.yaml*: Documentación OpenAPI con el contrato de la API.
 *.env.example*: Plantilla con las variables de entorno necesarias.
 *app.py*: Archivo principal para iniciar la aplicación.
 *requirements.txt*: Dependencias del proyecto.
 *virtualenv-setup.sh*: Script para automatizar la configuración del entorno.

----
# -Instalación-
Para instalar el proyecto se puede crear un entorno virtual:

bash
python -m venv .venv

Luego se activa el entorno virtual.

En Windows:
bash
.venv\Scripts\activate

En Linux/macOS:
bash
source .venv/bin/activate

Con el entorno activado, se instalan las dependencias:
bash
pip install -r requirements.txt

-----
# -Configuración-

Se debe crear un archivo .env tomando como referencia .env.example y completar los datos necesarios para la conexión con MySQL.

Para crear la base de datos se debe ejecutar el script:

text
db/init_db.sql
