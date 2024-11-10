import pandas as pd
from flask import Flask, render_template, request, redirect, url_for
from models import Socio, Cuota, session

app = Flask(__name__)

# Ruta para el home
@app.route('/')
def home():
    return render_template('base.html')

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

# Ruta para listar socios
@app.route('/socios')
def listar_socios():
    socios = session.query(Socio).all()
    return render_template('socios.html', socios=socios)

# Ruta para agregar un socio
@app.route('/socio/agregar', methods=['GET', 'POST'])
def agregar_socio():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        nuevo_socio = Socio(nombre=nombre, email=email)
        session.add(nuevo_socio)
        session.commit()
        return redirect(url_for('listar_socios'))
    return render_template('agregar_socio.html')

# Ruta para editar un socio
@app.route('/socio/editar/<int:id_socio>', methods=['GET', 'POST'])
def editar_socio(id_socio):
    socio = session.query(Socio).get(id_socio)
    if request.method == 'POST':
        socio.nombre = request.form['nombre']
        socio.email = request.form['email']
        session.commit()
        return redirect(url_for('listar_socios'))
    return render_template('editar_socio.html', socio=socio)

# Ruta para eliminar un socio
@app.route('/socio/eliminar/<int:id_socio>')
def eliminar_socio(id_socio):
    socio = session.query(Socio).get(id_socio)
    session.delete(socio)
    session.commit()
    return redirect(url_for('listar_socios'))

# Ruta para ver cuotas de un socio
@app.route('/cuotas/<int:id_socio>')
def ver_cuotas(id_socio):
    socio = session.query(Socio).get(id_socio)
    return render_template('cuotas.html', socio=socio)

@app.route('/cuotas_lista')
def listar_cuotas():
    cuotas = session.query(Cuota).all()  # Obtiene todas las cuotas de la base de datos
    return render_template('cuotas_lista.html', cuotas=cuotas)    

# Ruta para agregar una cuota
@app.route('/cuota/agregar/<int:id_socio>', methods=['GET', 'POST'])
def agregar_cuota(id_socio):
    if request.method == 'POST':
        monto = request.form['monto']
        fecha_vencimiento = request.form['fecha_vencimiento']
        nueva_cuota = Cuota(id_socio=id_socio, monto=monto, fecha_vencimiento=fecha_vencimiento)
        session.add(nueva_cuota)
        session.commit()
        return redirect(url_for('ver_cuotas', id_socio=id_socio))
    return render_template('agregar_cuota.html', id_socio=id_socio)

@app.route('/socio/cargar_csv', methods=['GET', 'POST'])
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

        # Lee el archivo CSV usando pandas
        datos = pd.read_csv(archivo)

        # Itera cada fila e inserta los datos en la base de datos si no son duplicados
        for _, fila in datos.iterrows():
            # Verificar si el email ya existe en la base de datos
            socio_existente = session.query(Socio).filter_by(email=fila['email']).first()
            if socio_existente:
                flash(f'El socio con email {fila["email"]} ya existe y no fue agregado.', 'info')
                continue  # Saltar a la siguiente fila si el socio ya existe

            # Crear el nuevo objeto Socio
            nuevo_socio = Socio(
                name=fila['name'],
                email=fila['email'],
                phone=fila.get('phone', '')  # Usar un valor vacío si no existe el campo phone
            )
            session.add(nuevo_socio)

        # Guardar todos los cambios
        session.commit()
        flash('Datos del archivo CSV agregados exitosamente', 'success')
        return redirect(url_for('listar_socios'))

    return render_template('cargar_csv.html')




if __name__ == '__main__':
    #app.run(debug=True)
    app.run(debug=True, host="0.0.0.0", port=8080)
