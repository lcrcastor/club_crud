CREATE TABLE socios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20)
);

CREATE TABLE cuotas (
    id_cuota INT AUTO_INCREMENT PRIMARY KEY,
    id_socio INT NOT NULL,
    monto FLOAT NOT NULL,
    fecha_vencimiento DATE NOT NULL,
    pagada BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (id_socio) REFERENCES socios(id)
);
