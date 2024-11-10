from flask import Blueprint, render_template, request, redirect, url_for
from models import session, Cuota, Socio

cuota_bp = Blueprint('cuota', __name__)

# Ruta para ver cuotas de un socio
@cuota_bp.route('/cuotas/<int:id_socio>')
def ver_cuotas(id_socio):
    socio = session.query(Socio).get(id_socio)
    return render_template('cuotas.html', socio=socio)

# Ruta para listar todas las cuotas
@cuota_bp.route('/cuotas_lista')
def listar_cuotas():
    cuotas = session.query(Cuota).all()
    return render_template('cuotas_lista.html', cuotas=cuotas)

# Ruta para agregar una cuota
@cuota_bp.route('/cuota/agregar/<int:id_socio>', methods=['GET', 'POST'])
def agregar_cuota(id_socio):
    if request.method == 'POST':
        monto = request.form['monto']
        fecha_vencimiento = request.form['fecha_vencimiento']
        nueva_cuota = Cuota(id_socio=id_socio, monto=monto, fecha_vencimiento=fecha_vencimiento)
        session.add(nueva_cuota)
        session.commit()
        return redirect(url_for('cuota.ver_cuotas', id_socio=id_socio))
    return render_template('agregar_cuota.html', id_socio=id_socio)
