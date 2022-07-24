"""
    Script encargado de inicializar la base de datos y gestionar las migraciones
    en el arranque del contenedor
"""
import pymysql
import os

from src.config import db_settings
from src.util.authentication import encode_password, generate_salt

# SQL QUERIES
SQL_CREATE_DATABASE = "CREATE DATABASE IF NOT EXISTS {database}"
SQL_GRANT_DATABASE = "GRANT ALL PRIVILEGES ON {database}.* TO {user}@\"%\""
SQL_INSERT_ADMIN = "INSERT IGNORE INTO `{database}`.`usuarios` (`id_user`, `username`, `password`, `email`, `es_admin`, `activo`, `salt`) VALUES \
    ('1', 'admin', '{password}', 'admin@irrigation.gal', '1', '1', '{salt}');"
# just for testing, comment when deploying
SQL_INSERT_GUEST = "INSERT IGNORE INTO `{database}`.`usuarios` (`id_user`, `username`, `password`, `email`, `es_admin`, `activo`, `salt`) VALUES \
    ('2', 'guest', '{password}', 'guest@irrigation.gal', '0', '1', '{salt}');"


def execute_query(query: str) -> None:
    conn = pymysql.connect(
        user=db_settings.ROOT_USER,
        port=db_settings.PORT,
        host=db_settings.HOST,
        password=db_settings.ROOT_PASSWORD
    )
    conn.cursor().execute(query)
    conn.commit()
    conn.close()


# creación de la base de datos
execute_query(
    SQL_CREATE_DATABASE.format(database=db_settings.DATABASE)
)
execute_query(
    SQL_GRANT_DATABASE.format(
        user=db_settings.USER,
        database=db_settings.DATABASE
    )
)


# ejecutamos las migraciones
os.system("pem migrate")


# añadimos usuario admin
salt = generate_salt()
execute_query(
    SQL_INSERT_ADMIN.format(
        database=db_settings.DATABASE,
        password=encode_password(db_settings.USER_ADMIN_PASSWORD, salt),
        salt=salt
    )
)
# añadimos usuario guest
salt = generate_salt()
execute_query(
    SQL_INSERT_GUEST.format(
        database=db_settings.DATABASE,
        password=encode_password("guest", salt),
        salt=salt
    )
)