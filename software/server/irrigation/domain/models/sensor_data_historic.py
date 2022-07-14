# -*- coding: utf-8 -*-
import attr

from domain.models.historic import HistoricData, QueryHistoricData


@attr.s
class SensorData(HistoricData):
    humidity: float = attr.ib(default=0.0)
    temperature: float = attr.ib(default=0.0)
    raining: bool = attr.ib(default=False)

    def __dict__(self) -> dict:
        return {
            'controller_id': self.controller_id,
            'controller': self.controller,
            'area_id': self.area_id,
            'area': self.area,
            'humidity': self.humidity,
            'temperature': self.temperature,
            'raining': self.raining,
            'date': self.date,
        }


@attr.s
class QuerySensorData(QueryHistoricData):
    humidity: float = attr.ib(default=None)
    temperature: float = attr.ib(default=None)
    raining: bool = attr.ib(default=None)

    def get_equal_values(self):
        fields = []

        if self.controller_id is not None:
            fields.append('controller_id')
        if self.area_id is not None:
            fields.append('area_id')

        return fields

    def get_greater_equals_than_values(self):
        fields = []

        if self.humidity is not None:
            fields.append('humidity')
        if self.temperature is not None:
            fields.append('temperature')
        if self.raining is not None:
            fields.append('raining')

        return fields
