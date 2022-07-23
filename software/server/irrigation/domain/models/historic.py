# -*- coding: utf-8 -*-
import attr


@attr.s
class HistoricData():
    """ Data stored by all historics
    """
    controller_id: int = attr.ib()
    controller: str = attr.ib()
    area_id: int = attr.ib()
    area: str = attr.ib()
    date: str = attr.ib(default=None)


@attr.s
class QueryHistoricData():
    controller_id: int = attr.ib(default=None)
    area_id: int = attr.ib(default=None)
    start_date: str = attr.ib(default=None)
    end_date: str = attr.ib(default=None)
