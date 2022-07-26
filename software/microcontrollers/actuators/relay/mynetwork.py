import machine
import network
import time


class NetworkManager():

    def __init__(self, ssid: str, pw: str) -> None:
        print("setting up NetworkManager...")
        self.ssid = ssid
        self.pw = pw

        # setting up config
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)

    def light_onboard_led(self) -> None:
        self.led = machine.Pin('LED', machine.Pin.OUT)
        self.led.on()

    def connect(self) -> Exception:
        # connecting ...
        self.wlan.connect(self.ssid, self.pw)
        timeout = 10

        # checking connection status
        while timeout > 0:
            if self.wlan.status() >= 3:
                self.light_onboard_led()
                break
            timeout -= 1
            print('waiting for connection...')
            time.sleep(1)

        if self.wlan.status() != 3:
            raise RuntimeError('network connection failed')
        else:
            print('connected')
            status = self.wlan.ifconfig()
            print('ip = ' + status[0])
