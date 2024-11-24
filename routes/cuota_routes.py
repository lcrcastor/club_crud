from flask import Blueprint, render_template, request, redirect, url_for
from models import session, Cuota, Socio

cuota_bp = Blueprint('cuota', __name__)

# Ruta para ver cuotas de un socio
@cuota_bp.route('/cuotas/<int:id_socio>', methods=['GET', 'POST'])
def ver_cuotas(id_socio):
    #id = id_socio
    socio = session.query(Socio).get(id_socio)
    #cuotas = session.query(Cuota).get(id_socio)
    cuotas = session.query(Cuota).filter_by(id_socio=id_socio).all()
    #lista de cotas por socio 
    print("DAtos de cuota: ")
    print (cuotas)
    # se le pueden pasar mas de un objeto 
    return render_template('ver_cuotas.html', cuota=cuotas, socio=socio)

# Ruta para listar todas las cuotas
@cuota_bp.route('/cuotas_lista')
def listar_cuotas():
    cuotas = session.query(Cuota).all()
    if not cuotas:
        cuotas = {}
    return render_template('cuotas_lista.html', cuota=cuotas)

# Ruta para agregar una cuota
@cuota_bp.route('/cuota/agregar/<int:id>', methods=['GET', 'POST'])
def agregar_cuota(id):
    if request.method == 'POST':
        socio = session.query(Socio).get(id)
        monto = request.form['monto']
        fecha = request.form['fecha']
        nueva_cuota = Cuota(id_socio=id, monto=monto, fecha=fecha)
        session.add(nueva_cuota)
        session.commit()
        cuota = session.query(Cuota).get(id_socio)
        return redirect(url_for('cuota.ver_cuotas', socio=socio ,cuota=cuota))
    return render_template('agregar_cuota.html', id=id)

