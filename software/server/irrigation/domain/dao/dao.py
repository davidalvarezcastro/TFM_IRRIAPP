# -*- coding: utf-8 -*-
import attr


from domain.dao.database import DatabaseInterface


@attr.s
class DAO():
    """  Data Access Object """
    db: DatabaseInterface = attr.ib()
