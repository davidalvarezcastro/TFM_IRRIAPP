
from domain.models.irrigation_actuator_algorithm import IrrigationActivateActuator
from application.actuator.models.interface_actuator_irrigation import InterfaceActuatorIrirgationHandler


class SimpleActuatorIrirgationHandler(InterfaceActuatorIrirgationHandler):
    """
        Algorithm to resolve if it is necessary to activate the actuator (very simple)
    """

    def check_activate_irrigation(self, query: IrrigationActivateActuator) -> bool:

        if query.rainning < 35:
            if query.temperature > 35:
                return query.humidity < 30
            elif query.temperature > 30:
                return query.humidity < 45
            else:
                return query.humidity < 60

        return False
