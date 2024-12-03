from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import session, Socio, db_session
import pandas as pd
from sqlalchemy.exc import IntegrityError

# Definir el Blueprint para la ruta de socios 
socio_bp = Blueprint('socio', __name__)


# Función para insertar socios en la base de datos
def insertar_socios(socios_nuevos):
    for fila in socios_nuevos:
        nuevo_socio = Socio(
            id=fila['id'],
            nro_documento=fila['nro_documento'],
            name=fila['name'],
            email=fila['email'],
            phone=fila['phone']
        )
        session.add(nuevo_socio)
        try:
            session.commit()
        except IntegrityError:
            # Realizar rollback si se detecta un duplicado y continuar con el siguiente
            session.rollback()
            flash(f'Socio con ID {fila["id"]} ya existe y no fue agregado.', 'info')
    flash("Datos del CSV procesados exitosamente", "success")
    return redirect(url_for('socio.listar_socios'))


# Ruta para listar socios
@socio_bp.route('/socios')
def listar_socios():
    socios = session.query(Socio).all()
    if not socios:
        socios = {}
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
    return render_template('socio.agregar_socio.html')

# Ruta para editar un socio
@socio_bp.route('/socio/editar/<int:id>', methods=['GET', 'POST'])
def editar_socio(id):
    #socio = session.query.get_or_404(id)
    socio = session.query(Socio).get(id)
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        phone = request.form['phone']

        # Validación del teléfono
        import re
        if not re.match(r'^\d{8}$', phone):
            flash('Número de teléfono inválido. Formato requerido: 4567890.', 'error')
            return render_template('editar_socio.html', socio=socio)

        # Actualizar datos
        socio.name = nombre
        socio.email = email
        socio.phone = phone
        db_session.commit()
        flash('Datos actualizados con éxito.', 'success')
        return redirect(url_for('socio.listar_socios')) # Redirecciona a la lista de socios
     
    return render_template('editar_socio.html', socio=socio)



# Ruta para eliminar un socio
@socio_bp.route('/socio/eliminar/<int:id>')
def eliminar_socio(id):
    socio = session.query(Socio).get(id)
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

        # Remover filas duplicadas basadas en la columna 'id' en el CSV
        datos = datos.drop_duplicates(subset=['id'])

        # Si 'nro_documento' no está en las columnas, asignar el valor de 'id' a 'nro_documento'
        #if 'nro_documento' not in datos.columns:
        #    datos['nro_documento'] = datos['id']  # Asigna el valor de 'id' a 'nro_documento'
        # Reemplazar NaN con None en las columnas 'nro_documento', 'email' y 'phone'
        
        datos['email'] = datos['email'].apply(lambda x: None if pd.isna(x) else x)
        datos['phone'] = datos['phone'].apply(lambda x: None if pd.isna(x) else x)
        datos['nro_documento'] = datos['id'].apply(lambda x: None if pd.isna(x) else x)

        ids_duplicados = []
        socios_nuevos = []
        
        print("contenido de datos:")
        print(datos)
        print("---------------------------------------")
        for _, fila in datos.iterrows():
            # Verificar si el socio con el mismo `id` ya existe en la base de datos
            socio_existente = db_session.query(Socio).filter_by(id=fila['id']).first()
            if socio_existente:
                ids_duplicados.append(fila)
            else:
                socios_nuevos.append(fila)

        # Informar al usuario sobre los ID duplicados encontrados
        if ids_duplicados:
            flash(f'Se encontraron {len(ids_duplicados)} IDs duplicados que no serán procesados.', 'info')

        # Insertar los socios nuevos que no tienen ID duplicados en el CSV ni en la base de datos
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

    # Insertar cada socio que no fue descartado tener en cuenta que se se agrega el campo nro_documento
    for socio in socios_a_insertar:
        nuevo_socio = Socio(
            id=socio['id'],
            nro_documento=socio['nro_documento'],
            name=socio['name'],
            email=socio['email'],
            phone=socio['phone']
        )
        session.add(nuevo_socio)
    
    session.commit()
    flash("Datos del CSV procesados exitosamente", "success")
    return redirect(url_for('socio.listar_socios'))
