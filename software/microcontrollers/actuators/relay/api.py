import json
import socket

from relay import Controller
from globals import API_HOST, API_PORT, API_TURN_OFF, API_TURN_ON


class ApiRest():

    def __init__(self, host: str = API_HOST, port: int = API_PORT, controller: Controller = None) -> Exception:
        if controller is None:
            raise Exception('controller not defined!')

        self.host = host
        self.port = port
        self.controller = controller

        # setup & open socket
        addr = socket.getaddrinfo(self.host, self.port)[0][-1]
        self.s = socket.socket()
        self.s.bind(addr)
        self.s.listen(1)

    def run(self) -> Exception:
        # listen for connections
        while True:
            try:
                response = {}
                # default response
                status = "error"
                msg = "something went wrong!"

                cl, addr = self.s.accept()
                print('client connected from', addr)

                request = cl.recv(1024)  # receiving 1024 bytes (enought for these endoints)

                request = str(request)
                relay_on = request.find(API_TURN_ON)
                print('relay on = ' + str(relay_on))
                relay_off = request.find(API_TURN_OFF)
                print('relay off = ' + str(relay_off))

                if relay_on == 6:
                    print("relay on")
                    self.controller.on()
                    status = "success"
                    msg = "Relay is ON"

                if relay_off == 6:
                    print("relay off")
                    self.controller.off()
                    status = "success"
                    msg = "Relay is OFF"

                response['status'] = status
                response['msg'] = msg
                cl.send('HTTP/1.0 200 OK\r\nContent-type: application/json\r\n\r\n')
                cl.send(json.dumps(response).encode('utf-8'))
                cl.close()

            except OSError as e:
                cl.close()
                print('connection closed')
