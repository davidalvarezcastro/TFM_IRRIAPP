import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


from domain.models.irrigation_actuator_algorithm import IrrigationActivateActuator
from application.actuator.models.interface_actuator_irrigation import InterfaceActuatorIrirgationHandler


class FuzzyLogicActuatorIrirgationHandler(InterfaceActuatorIrirgationHandler):
    """
        Fuzzy logic-based algorithm to resolve if it is necessary to activate the actuator
    """

    def __init__(self) -> None:
        super().__init__()

        self.max_value_raining = 100
        self.max_value_humidity = 100
        self.max_value_temperature = 60  # 56.7 ºC at USA (top record temperature on Earth)
        self.max_value_irrigation = 100  # change it when using ml instead bool value

        # generate universe
        self._generate_fuzzy_logic_space()

    def _generate_fuzzy_logic_space(self):
        # variables
        self.raining = ctrl.Antecedent(np.arange(0, self.max_value_raining, 1), 'raining')
        self.humidity = ctrl.Antecedent(np.arange(0, self.max_value_humidity, 1), 'humidity')
        self.temperature = ctrl.Antecedent(np.arange(0, self.max_value_temperature, 1), 'temperature')
        self.irrigate = ctrl.Consequent(np.arange(0, self.max_value_irrigation, 1), 'irrigate')

        # membership functions
        self.temperature['low'] = fuzz.trapmf(self.temperature.universe, [0, 0, 5, 15])
        self.temperature['medium'] = fuzz.trimf(self.temperature.universe, [5, 18, 26])
        self.temperature['high'] = fuzz.trapmf(self.temperature.universe,
                                               [20, 35, self.max_value_temperature, self.max_value_temperature])
        self.humidity['low'] = fuzz.trapmf(self.humidity.universe, [0, 0, 30, 50])
        self.humidity['medium'] = fuzz.trapmf(self.humidity.universe, [40, 50, 60, 70])
        self.humidity['high'] = fuzz.trapmf(self.humidity.universe,
                                            [60, 90, self.max_value_humidity, self.max_value_humidity])
        self.raining['low'] = fuzz.trapmf(self.raining.universe, [0, 0, 50, 60])
        self.raining['high'] = fuzz.trapmf(self.raining.universe,
                                           [50, 80, self.max_value_raining, self.max_value_raining])
        self.irrigate['low'] = fuzz.trapmf(self.irrigate.universe, [0, 0, 35, 40])
        self.irrigate['high'] = fuzz.trapmf(self.irrigate.universe,
                                            [35, 50, self.max_value_irrigation, self.max_value_irrigation])

        # define rules
        r1 = ctrl.Rule(
            antecedent=(self.raining['high']),
            consequent=(self.irrigate['low'])
        )
        r2 = ctrl.Rule(
            antecedent=(self.raining['low'] & self.humidity['low'] & self.temperature['high']),
            consequent=(self.irrigate['high'])
        )
        r3 = ctrl.Rule(
            antecedent=(self.raining['low'] & self.humidity['low'] & self.temperature['medium']),
            consequent=(self.irrigate['high'])
        )
        r4 = ctrl.Rule(
            antecedent=(self.raining['low'] & self.humidity['low'] & self.temperature['low']),
            consequent=(self.irrigate['high'])
        )
        r5 = ctrl.Rule(
            antecedent=(self.raining['low'] & self.humidity['medium'] & self.temperature['high']),
            consequent=(self.irrigate['low'])
        )
        r6 = ctrl.Rule(
            antecedent=(self.raining['low'] & self.humidity['medium'] & self.temperature['medium']),
            consequent=(self.irrigate['high'])
        )
        r7 = ctrl.Rule(
            antecedent=(self.raining['low'] & self.humidity['medium'] & self.temperature['low']),
            consequent=(self.irrigate['low'])
        )
        r8 = ctrl.Rule(
            antecedent=(self.raining['low'] & self.humidity['high'] & self.temperature['high']),
            consequent=(self.irrigate['low'])
        )
        r9 = ctrl.Rule(
            antecedent=(self.raining['low'] & self.humidity['high'] & self.temperature['medium']),
            consequent=(self.irrigate['low'])
        )
        r10 = ctrl.Rule(
            antecedent=(self.raining['low'] & self.humidity['high'] & self.temperature['low']),
            consequent=(self.irrigate['low'])
        )

        rules = [
            r1, r2, r3, r4, r5, r6, r7, r8, r9, r10
            # r11, r12, r13, r14, r15, r16, r17, r18, r19, r20,
            # r21, r22, r23, r24, r25, r26, r27
        ]

        # inference system
        tipping_ctrl = ctrl.ControlSystem(rules)

        # skfuzzy for simulation
        self.tipping = ctrl.ControlSystemSimulation(tipping_ctrl)

    def check_activate_irrigation(self, query: IrrigationActivateActuator) -> bool:

        self.tipping.input['raining'] = query.rainning
        self.tipping.input['temperature'] = query.temperature
        self.tipping.input['humidity'] = query.humidity

        self.tipping.compute()

        print("\n\n")
        print(query)
        print(self.tipping.output['irrigate'])
        print("\n\n")
        return False
