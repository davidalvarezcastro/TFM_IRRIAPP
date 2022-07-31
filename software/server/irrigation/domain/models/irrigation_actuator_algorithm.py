import attr


@attr.s
class IrrigationActivateActuator():
    rainning: bool = attr.ib(default=True)
    humidity: float = attr.ib(default=0.0)
    temperature: float = attr.ib(default=0.0)
