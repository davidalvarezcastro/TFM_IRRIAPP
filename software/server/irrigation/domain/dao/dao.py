# -*- coding: utf-8 -*-
import attr


from domain.dao.database import InterfazDatabase

@attr.s
class DAO():
    """ Clase padre para gestionar los Data Access Object """
    db: InterfazDatabase = attr.ib() # instancia conector base de datos
