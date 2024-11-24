import importlib.util
from sqlalchemy import create_engine
from sqlalchemy.schema import CreateTable
from pathlib import Path


def load_model_file(model_file: str):
    """
    Carga dinámicamente el archivo de modelos como módulo.
    :param model_file: Ruta al archivo .py que contiene los modelos.
    :return: Módulo cargado.
    """
    try:
        module_name = Path(model_file).stem  # Nombre del módulo (sin extensión)
        spec = importlib.util.spec_from_file_location(module_name, model_file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    except Exception as e:
        raise RuntimeError(f"Error al cargar el archivo de modelos '{model_file}': {e}")


def clean_sql_statement(sql: str) -> str:
    """
    Limpia y formatea una sentencia SQL para garantizar que termine correctamente con ';'.
    :param sql: Sentencia SQL generada.
    :return: Sentencia SQL limpia y corregida.
    """
    sql = sql.strip()
    if sql.endswith(");"):  # Caso correcto, no hacer nada
        return sql
    if sql.endswith(")"):  # Falta el ';', agregarlo
        return sql + ";"
    return sql  # En caso de sentencias adicionales


def generate_init_sql(model_file: str, output_file: str, database_name: str):
    """
    Genera el archivo init.sql para inicializar la base de datos MySQL.
    :param model_file: Ruta al archivo .py con los modelos.
    :param output_file: Nombre del archivo de salida (init.sql).
    :param database_name: Nombre de la base de datos MySQL.
    """
    try:
        # Cargar el archivo de modelos
        models = load_model_file(model_file)

        # Verificar que contiene la base de modelos
        if not hasattr(models, 'Base'):
            raise ValueError(f"El archivo '{model_file}' no define 'Base' como instancia de SQLAlchemy.")

        # Configurar el motor MySQL (para generar el SQL correcto)
        engine = create_engine("mysql+pymysql://root:password@localhost:3306")

        # Abrir el archivo de salida
        with open(output_file, "w") as f:
            # Crear la base de datos y usarla
            f.write(f"CREATE DATABASE IF NOT EXISTS {database_name};\n")
            f.write(f"USE {database_name};\n\n")

            # Recorrer y generar el SQL para cada tabla
            for table in models.Base.metadata.sorted_tables:
                sql = str(CreateTable(table).compile(engine))
                sql = clean_sql_statement(sql)
                f.write(f"{sql}\n\n")

            print(f"Archivo '{output_file}' generado con éxito.")
    except Exception as e:
        print(f"Error durante la generación del archivo 'init.sql': {e}")


if __name__ == "__main__":
    # Configuración
    MODEL_FILE = "models.py"          # Ruta al archivo con los modelos
    OUTPUT_FILE = "init_db.sql"          # Nombre del archivo de salida
    DATABASE_NAME = "club_database"   # Nombre de la base de datos

    generate_init_sql(MODEL_FILE, OUTPUT_FILE, DATABASE_NAME)
