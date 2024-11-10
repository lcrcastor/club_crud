from flask import Blueprint, render_template

general_bp = Blueprint('general', __name__)

# Ruta para el home
@general_bp.route('/')
def home():
    return render_template('base.html')

@general_bp.route('/contacto')
def contacto():
    return render_template('contacto.html')
