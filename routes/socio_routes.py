from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import session, Socio
import pandas as pd

# Definir el Blueprint para la ruta de socios 
socio_bp = Blueprint('socio', __name__)


# Función para insertar socios en la base de datos
def insertar_socios(socios_nuevos):
    for fila in socios_nuevos:
        nuevo_socio = Socio(
            id=fila['id'],
            name=fila['name'],
            email=fila['email'],
            phone=fila['phone']
        )
        session.add(nuevo_socio)
    
    session.commit()
    flash("Datos del CSV procesados exitosamente", "success")
    return redirect(url_for('socio.listar_socios'))

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

# Ruta para cargar el csv de nomina 
@socio_bp.route('/socio/cargar_csv', methods=['GET', 'POST'])
def cargar_csv():
    if request.method == 'POST':
        archivo = request.files.get('archivo_csv')
        
        if not archivo or not archivo.filename.endswith('.csv'):
            flash('Por favor, sube un archivo CSV', 'error')
            return redirect(request.url)

        # Leer el archivo CSV y usar la primera fila como encabezado
        datos = pd.read_csv(archivo, header=0)

        # Verificar que la columna 'id' exista en el CSV
        if 'id' not in datos.columns:
            flash('El archivo CSV debe contener una columna "id".', 'error')
            return redirect(request.url)

        datos['email'] = datos['email'].apply(lambda x: None if pd.isna(x) else x)
        datos['phone'] = datos['phone'].apply(lambda x: None if pd.isna(x) else x)

        ids_duplicados = []
        socios_nuevos = []
        
        for _, fila in datos.iterrows():
            try:
                socio_existente = session.query(Socio).filter_by(id=fila['id']).first()
                if socio_existente:
                    ids_duplicados.append(fila)
                else:
                    socios_nuevos.append(fila)
            except Exception as e:
                session.rollback()  # Realiza el rollback en caso de un error
                flash(f'Error al procesar el archivo: {str(e)}', 'error')
                return redirect(request.url)

        if ids_duplicados:
            session['socios_nuevos'] = [fila.to_dict() for fila in socios_nuevos]
            return render_template(
                'confirmar_csv.html',
                ids_duplicados=ids_duplicados,
                socios_nuevos=socios_nuevos
            )

        return insertar_socios(socios_nuevos)

    return render_template('cargar_csv.html')


@socio_bp.route('/socio/confirmar_carga_csv', methods=['POST'])
def confirmar_carga_csv():
    # Obtener los IDs que el usuario desea descartar
    ids_descartados = request.form.getlist('descartar_ids')
    
    # Procesar los socios restantes para insertar en la base de datos
    socios_a_insertar = [
        socio for socio in session['socios_nuevos']
        if str(socio['id']) not in ids_descartados
    ]

    # Insertar cada socio que no fue descartado
    for socio in socios_a_insertar:
        nuevo_socio = Socio(
            id=socio['id_socio'],
            name=socio['name'],
            email=socio['email'],
            phone=socio['phone']
        )
        session.add(nuevo_socio)
    
    session.commit()
    flash("Datos del CSV procesados exitosamente", "success")
    return redirect(url_for('socio.listar_socios'))

