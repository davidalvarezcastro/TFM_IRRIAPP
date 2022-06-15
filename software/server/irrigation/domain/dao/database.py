# -*- coding: utf-8 -*-
import typing
import attr
import logging
import mysql.connector
from mysql.connector import errorcode
from abc import ABC, abstractmethod


from utils import Log


_LOGGER = Log(logger=logging.getLogger('irrigation'))


class InterfazDatabase(ABC):
    """
    Interfaz de comunicación con una base de datos (conector a DB)
    """

    @abstractmethod
    def init_connection(self) -> None:
        """
        Función para iniciar una conexión con la base de datos

        Args:
        Raise:
            Exception
        """
        raise Exception("NotImplementedException")

    @abstractmethod
    def close_connection(self) -> None:
        """
        Función para cerrar una conexión con la base de datos

        Args:
        Raise:
            Exception
        """
        raise Exception("NotImplementedException")

    @abstractmethod
    def query(self, sql: str, params: typing.Tuple[str]=()) -> typing.Any:
        """Ejecuta una consulta SQL genérica.

        Args:
            sql (str): consulta sql
            params (typing.Tuple[str]): listado de parámetros
        Raise:
            Exception
        """
        raise Exception("NotImplementedException")

    @abstractmethod
    def delete(self, sql: str, params: typing.Tuple[str]=()) -> bool:
        """Ejecuta una consulta SQL para eliminar registros.

        Args:
            sql (str): consulta sql
            params (typing.Tuple[str]): listado de parámetros
        Raise:
            Exception
        """
        raise Exception("NotImplementedException")

    @abstractmethod
    def select(self, sql: str, params: typing.Tuple[str]=()) -> typing.List[typing.Tuple[typing.Any]]:
        """Ejecuta una consulta SQL para recuperar una serie de registros.

        Args:
            sql (str): consulta sql
            params (typing.Tuple[str]): listado de parámetros
        Raise:
            Exception
        """
        raise Exception("NotImplementedException")

    @abstractmethod
    def update(self, sql: str, params: typing.Tuple[str]=()) -> typing.List[typing.Tuple[typing.Any]]:
        """Ejecuta una consulta SQL para actualizar una serie de registros.

        Args:
            sql (str): consulta sql
            params (typing.Tuple[str]): listado de parámetros
        Raise:
            Exception
        """
        raise Exception("NotImplementedException")



@attr.s
class DatabaseConector(InterfazDatabase):
    host: str = attr.ib()
    port: int = attr.ib()
    _user: str = attr.ib()
    _password: str = attr.ib()
    database: str = attr.ib()
    new_connection: bool = attr.ib(default=False) # nueva conexión por consulta

    # POST INIT HOOK
    def __attrs_post_init__(self):
        pass

    # METHODS
    def init_connection(self):
        try:
            self.connector = mysql.connector.connect(
                host=self.host, port=self.port,
                user=self._user, password=self._password,
                database=self.database
            )
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                raise Exception(f"Problemas de conexión debido a las credenciales de conexión")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                raise Exception(f"La base de de datos {self.database} no existe")
            else:
                raise err

    def close_connection(self):
        try:
            if self.connector is not None:
                self.connector.close()
        except Exception:
            pass

    def _close(self):
        try:
            if self.connector is not None:
                self.cursor.close()
        except Exception:
            pass

    def query(self, sql: str, params: typing.Tuple[str]=()) -> typing.Any:
        try:
            if self.new_connection:
                self.init_connection()
            self.cursor = self.connector.cursor(
                dictionary=True,
                buffered=True,
            )
            self.cursor.execute(sql, params)
            return self.cursor
        except Exception as err:
            _LOGGER.error('database => query {} => {}'.format(sql, str(err)))
            try:
                self.connector.rollback()
            except Exception:
                pass
            return None

    def select(self, sql: str, params: typing.Tuple[str]=()) -> typing.List[typing.Tuple[typing.Any]]:
        try:
            result = None
            self.query(sql, params)
            result = self.cursor.fetchall()
            self.cursor.close()
            if self.new_connection:
                self.close_connection()
            return result
        except Exception as err:
            _LOGGER.error('database => select {} => {}'.format(sql, str(err)))
            return None

    def delete(self, sql: str, params: typing.Tuple[str]=()) -> bool:
        try:
            self.query(sql, params)
            self.connector.commit()
            self.cursor.close()
            if self.new_connection:
                self.close_connection()

            return True
        except Exception as err:
            _LOGGER.error('database => delete {} => {}'.format(sql, str(err)))
            return False

    def update(self, sql: str, params: typing.Tuple[str]=()) -> bool:
        try:
            self.query(sql, params)
            self.connector.commit()
            self.cursor.close()
            if self.new_connection:
                self.close_connection()

            return True
        except Exception as err:
            _LOGGER.error('database => update {} => {}'.format(sql, str(err)))
            return False

