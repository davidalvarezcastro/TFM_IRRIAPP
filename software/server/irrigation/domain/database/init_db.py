import pymysql

from settings import db_mysql_settings

# initialize database
SQL_CREATE_DATABASE = "CREATE DATABASE IF NOT EXISTS {database}"
SQL_GRANT_DATABASE = "GRANT ALL PRIVILEGES ON {database}.* TO {user}@\"%\""


def execute_query(query: str) -> None:
    conn = pymysql.connect(
        user="root",
        port=db_mysql_settings.PORT,
        host=db_mysql_settings.HOST,
        password=db_mysql_settings.ROOT_PASS
    )
    conn.cursor().execute(query)
    conn.commit()
    conn.close()


def init_db():
    # creación de la base de datos
    execute_query(
        SQL_CREATE_DATABASE.format(database=db_mysql_settings.DATABASE)
    )
    execute_query(
        SQL_GRANT_DATABASE.format(
            user=db_mysql_settings.USER,
            database=db_mysql_settings.DATABASE
        )
    )

    # import para crear las tablas
    import domain.database.models
