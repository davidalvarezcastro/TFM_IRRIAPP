# -*- coding: utf-8 -*-
import attr

from domain.models.actuator import ActuatorData


@attr.s
class IrrigationData(ActuatorData):
    irrigation: bool = attr.ib(default=True)  # will store amount of water in the future
