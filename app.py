from flask import Flask
from routes.socio_routes import socio_bp
from routes.cuota_routes import cuota_bp
from routes.general_routes import general_bp
app = Flask(__name__)



# Registrar los Blueprints
app.register_blueprint(socio_bp)
app.register_blueprint(cuota_bp)
app.register_blueprint(general_bp)



if __name__ == '__main__':
    #app.run(debug=True)
    app.run(debug=True, host="0.0.0.0", port=8080)
