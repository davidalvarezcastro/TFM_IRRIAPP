# -*- coding: utf-8 -*-
import attr

from domain.models.actuator import ActuatorData
from domain.models.historic import QueryHistoricData


@attr.s
class IrrigationData(ActuatorData):
    irrigation: bool = attr.ib(default=True)  # will store amount of water in the future

    def __dict__(self) -> dict:
        return {
            'area_id': self.area_id,
            'area': self.area,
            'irrigation': self.irrigation,
            'start_date': self.start_date,
            'end_date': self.end_date,
        }


@attr.s
class QueryIrrigationData(QueryHistoricData):
    irrigation: bool = attr.ib(default=True)
