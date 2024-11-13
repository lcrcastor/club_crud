from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import session, Socio, db_session,MovimientoCaja
import pandas as pd
from sqlalchemy.exc import IntegrityError
from datetime import datetime

# Definir el Blueprint para la ruta de socios 
movimientos_bp = Blueprint('movimientos', __name__)

@movimientos_bp.route('/movimientos')
def mostrar_movimientos():
    movimientos = db_session.query(MovimientoCaja).all()
    return render_template('movimientos.html', movimientos=movimientos)

@movimientos_bp.route('/movimiento/agregar', methods=['GET', 'POST'])
def agregar_movimiento():
    if request.method == 'POST':
        fecha = request.form['fecha']
        tipo = request.form['tipo']
        descripcion = request.form['descripcion']
        monto = float(request.form['monto'])
        
        nuevo_movimiento = MovimientoCaja(
            fecha=datetime.strptime(fecha, '%Y-%m-%d'),
            tipo=tipo,
            descripcion=descripcion,
            monto=monto
        )
        
        db_session.add(nuevo_movimiento)
        db_session.commit()
        flash('Movimiento registrado exitosamente.')
        return redirect(url_for('movimientos.mostrar_movimientos'))
    
    return render_template('agregar_movimiento.html')

@movimientos_bp.route('/movimiento/editar/<int:id>', methods=['GET', 'POST'])
def editar_movimiento(id):
    movimiento = db_session.query(MovimientoCaja).get(id)
    if not movimiento:
        flash('Movimiento no encontrado.')
        return redirect(url_for('movimientos.mostrar_movimientos'))

    if request.method == 'POST':
        movimiento.fecha = datetime.strptime(request.form['fecha'], '%Y-%m-%d')
        movimiento.tipo = request.form['tipo']
        movimiento.descripcion = request.form['descripcion']
        movimiento.monto = float(request.form['monto'])

        db_session.commit()
        flash('Movimiento actualizado exitosamente.')
        return redirect(url_for('movimientos.mostrar_movimientos'))

    return render_template('editar_movimiento.html', movimiento=movimiento)
