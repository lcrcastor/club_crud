import os, json 
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker


# Utilizar la URL de la base de datos desde el entorno
#DATABASE_URL = os.getenv("DATABASE_URL", "mysql+mysqlconnector://club_user:club_password@mysql/club_database")
#engine = create_engine(DATABASE_URL, echo=True)

# Cargar configuración desde config.json
with open("config.json") as config_file:
    config = json.load(config_file)

# Acceder a la URL de la base de datos y otros valores de configuración
DATABASE_URL = config["DATABASE_URL"]
DEBUG = config["DEBUG"]
SECRET_KEY = config["SECRET_KEY"]
MAX_CONNECTIONS = config["MAX_CONNECTIONS"]

# Crear el motor de base de datos
engine = create_engine(DATABASE_URL, echo=DEBUG)


# Crear la sesión de SQLAlchemy
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db_session = SessionLocal()  # Instancia de sesión

# Crear la base de datos declarativa
Base = declarative_base()

# Definir las clases de los modelos
class Socio(Base):
    __tablename__ = 'socios'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20))  # Nuevo campo para el número de teléfono


class Cuota(Base):
    __tablename__ = 'cuotas'
    
    id_cuota = Column(Integer, primary_key=True)
    id_socio = Column(Integer, ForeignKey('socios.id'), nullable=False)
    monto = Column(Float, nullable=False)
    fecha_vencimiento = Column(Date, nullable=False)
    pagada = Column(Boolean, default=False)
    
    # Relación con Socio
    #socio = relationship("Socio", back_populates="cuotas")


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
