import machine


class Controller():

    def on(self) -> NotImplementedError:
        raise NotImplementedError('not implemented!')

    def off(self) -> NotImplementedError:
        raise NotImplementedError('not implemented!')


class RelayController(Controller):

    def __init__(self, pinout: int) -> None:
        self.pinout = pinout
        self.gpio = machine.Pin(self.pinout, machine.Pin.OUT)

    def on(self) -> Exception:
        self.gpio.value(1)

    def off(self) -> Exception:
        self.gpio.value(0)
