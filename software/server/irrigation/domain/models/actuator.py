# -*- coding: utf-8 -*-
import attr


@attr.s
class ActuatorData():
    """ Data stored by actuator
    """
    area_id: int = attr.ib()
    area: str = attr.ib()
    start_date: str = attr.ib(default=None)
    end_date: str = attr.ib(default=None)


@attr.s
class QueryActuatorData():
    area_id: int = attr.ib()
    start_date: str = attr.ib(default=None)
    end_date: str = attr.ib(default=None)
