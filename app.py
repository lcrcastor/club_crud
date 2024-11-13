from flask import Flask
from routes.socio_routes import socio_bp
from routes.cuota_routes import cuota_bp
from routes.general_routes import general_bp
from routes.movimientos_routes import movimientos_bp
        
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'


# Registrar los Blueprints
app.register_blueprint(socio_bp)
app.register_blueprint(cuota_bp)
app.register_blueprint(general_bp)
app.register_blueprint(movimientos_bp)



if __name__ == '__main__':
    #app.run(debug=True)
    app.run(debug=True, host="0.0.0.0", port=8080)
