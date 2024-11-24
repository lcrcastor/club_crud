CREATE DATABASE IF NOT EXISTS club_database;
USE club_database;

CREATE TABLE montos_cuotas (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	monto FLOAT NOT NULL, 
	fecha_inicio DATE NOT NULL, 
	fecha_fin DATE NOT NULL, 
	mes VARCHAR(100) NOT NULL, 
	PRIMARY KEY (id)
);

CREATE TABLE movimientos_caja (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	fecha DATE NOT NULL, 
	tipo VARCHAR(10) NOT NULL, 
	descripcion VARCHAR(255) NOT NULL, 
	monto FLOAT NOT NULL, 
	PRIMARY KEY (id)
);

CREATE TABLE socios (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	nro_documento INTEGER NOT NULL, 
	name VARCHAR(100) NOT NULL, 
	email VARCHAR(100) NOT NULL, 
	phone VARCHAR(20), 
	PRIMARY KEY (id), 
	UNIQUE (nro_documento), 
	UNIQUE (email)
);

CREATE TABLE tipos_socios (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	descripcion VARCHAR(100) NOT NULL, 
	PRIMARY KEY (id)
);

CREATE TABLE cuotas (
	id_cuota INTEGER NOT NULL AUTO_INCREMENT, 
	id_socio INTEGER NOT NULL, 
	monto FLOAT NOT NULL, 
	mes VARCHAR(100) NOT NULL, 
	fecha DATE NOT NULL, 
	pagada BOOL, 
	PRIMARY KEY (id_cuota), 
	FOREIGN KEY(id_socio) REFERENCES socios (id)
);
