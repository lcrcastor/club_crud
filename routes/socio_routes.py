from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import session, Socio
import pandas as pd

socio_bp = Blueprint('socio', __name__)

# Ruta para listar socios
@socio_bp.route('/socios')
def listar_socios():
    socios = session.query(Socio).all()
    return render_template('socios.html', socios=socios)

# Ruta para agregar un socio
@socio_bp.route('/socio/agregar', methods=['GET', 'POST'])
def agregar_socio():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        nuevo_socio = Socio(nombre=nombre, email=email)
        session.add(nuevo_socio)
        session.commit()
        return redirect(url_for('socio.listar_socios'))
    return render_template('agregar_socio.html')

# Ruta para editar un socio
@socio_bp.route('/socio/editar/<int:id_socio>', methods=['GET', 'POST'])
def editar_socio(id_socio):
    socio = session.query(Socio).get(id_socio)
    if request.method == 'POST':
        socio.nombre = request.form['nombre']
        socio.email = request.form['email']
        session.commit()
        return redirect(url_for('socio.listar_socios'))
    return render_template('editar_socio.html', socio=socio)

# Ruta para eliminar un socio
@socio_bp.route('/socio/eliminar/<int:id_socio>')
def eliminar_socio(id_socio):
    socio = session.query(Socio).get(id_socio)
    session.delete(socio)
    session.commit()
    return redirect(url_for('socio.listar_socios'))

# Ruta para cargar un archivo CSV
@socio_bp.route('/socio/cargar_csv', methods=['GET', 'POST'])
def cargar_csv():
    if request.method == 'POST':
        if 'archivo_csv' not in request.files:
            flash('No se seleccionó un archivo', 'error')
            return redirect(request.url)
        archivo = request.files['archivo_csv']
        if archivo.filename == '':
            flash('Nombre de archivo vacío', 'error')
            return redirect(request.url)
        if not archivo.filename.endswith('.csv'):
            flash('Por favor, sube un archivo CSV', 'error')
            return redirect(request.url)

        datos = pd.read_csv(archivo)
        for _, fila in datos.iterrows():
            socio_existente = session.query(Socio).filter_by(email=fila['email']).first()
            if socio_existente:
                flash(f'El socio con email {fila["email"]} ya existe y no fue agregado.', 'info')
                continue
            nuevo_socio = Socio(name=fila['name'], email=fila['email'], phone=fila.get('phone', ''))
            session.add(nuevo_socio)
        session.commit()
        flash('Datos del archivo CSV agregados exitosamente', 'success')
        return redirect(url_for('socio.listar_socios'))

    return render_template('cargar_csv.html')

