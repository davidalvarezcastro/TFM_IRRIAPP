# Controlador Sensores

Código del controlador para la lectura de los datos de sensores y el envío al sistema de comunicación asíncrona. El proyecto del microcontrolador se encuentra dividido en dos partes distintas:

- programa para la **lectura de datos** de los sensores (*Arduino*)
- programa encargado de **recibir los datos y enviarlos mediante wifi** al broker MQTT (*ESP8266*)
