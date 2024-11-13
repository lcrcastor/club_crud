-- init_db.sql

-- Crear la base de datos si no existe
CREATE DATABASE IF NOT EXISTS club_database;
USE club_database;

-- Crear la tabla socios con id como BIGINT
CREATE TABLE IF NOT EXISTS socios (
    id BIGINT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(20)
);

-- Crear la tabla cuotas si aún no existe
CREATE TABLE IF NOT EXISTS cuotas (
    id_cuota INT AUTO_INCREMENT PRIMARY KEY,
    id_socio BIGINT NOT NULL,
    monto FLOAT NOT NULL,
    fecha_vencimiento DATE NOT NULL,
    pagada BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (id_socio) REFERENCES socios(id)
);

-- Crear la tabla de movimientos de caja si no existe
CREATE TABLE IF NOT EXISTS movimientos_caja (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATE NOT NULL,
    tipo VARCHAR(10) CHECK (tipo IN ('ingreso', 'egreso')) NOT NULL,
    descripcion VARCHAR(255) NOT NULL,
    monto DECIMAL(10, 2) NOT NULL  -- Asegurarse de tener precisión adecuada para movimientos financieros
);