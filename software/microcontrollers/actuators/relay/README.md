# Relay actuator

Permite controlar la activación y desactivación de un relé mediante eventos MQTT.

## Eventos (*subscriber*)

### **/area/:area/relay/on**

Evento emitido por el servidor para activar el relé del actuador.

| **Type**  | **Topic**  | **Payload**  |
|--- |:---: |:---: |
| *COMMAND*  | /area/<span style="color: royalblue">:area</span>/relay/<span style="color: red">on</span>  | <span style="color: yellowgreen">{data}</span>  |

| **Type**  | **Params**  | **Value**  | **Description**  |
|--- |:---: |:---: |--- |
| *TOPIC_PARAM*  | <span style="color: royalblue">area</span>  | <span style="color: tan">Integer</span>  | Código identificativo de la zona a la que pertenece el actuador.  |
| *PAYLOAD*  | <span style="color: yellowgreen">data</span>  | <span style="color: tan">JSON</span>  | Datos (actualmente vacío)  |

**estado:**

```json
{}
```

### **/area/:area/relay/off**

Evento emitido por el servidor para desactivar el relé del actuador.

| **Type**  | **Topic**  | **Payload**  |
|--- |:---: |:---: |
| *COMMAND*  | /area/<span style="color: royalblue">:area</span>/relay/<span style="color: red">off</span>  | <span style="color: yellowgreen">{data}</span>  |

| **Type**  | **Params**  | **Value**  | **Description**  |
|--- |:---: |:---: |--- |
| *TOPIC_PARAM*  | <span style="color: royalblue">area</span>  | <span style="color: tan">Integer</span>  | Código identificativo de la zona a la que pertenece el actuador.  |
| *PAYLOAD*  | <span style="color: yellowgreen">data</span>  | <span style="color: tan">JSON</span>  | Datos (actualmente vacío)  |

**estado:**

```json
{}
```

## Eventos (*publisher*)

### **/area/:area/relay/on/ok**

Evento emitido por el actuador (gestionado por el servidor) para indicar que se ha procesado la orden de activación y el relé se ha activado.

| **Type**  | **Topic**  | **Payload**  |
|--- |:---: |:---: |
| *COMMAND*  | /area/<span style="color: royalblue">:area</span>/relay/<span style="color: red">on</span>/ok  | <span style="color: yellowgreen">{data}</span>  |

| **Type**  | **Params**  | **Value**  | **Description**  |
|--- |:---: |:---: |--- |
| *TOPIC_PARAM*  | <span style="color: royalblue">area</span>  | <span style="color: tan">Integer</span>  | Código identificativo de la zona a la que pertenece el actuador.  |
| *PAYLOAD*  | <span style="color: yellowgreen">data</span>  | <span style="color: tan">JSON</span>  | Datos (actualmente vacío)  |

**estado:**

```json
{}
```

### **/area/:area/relay/off/ok**

Evento emitido por el actuador (gestionado por el servidor) para indicar que se ha procesado la orden de desactivación y el relé se ha desactivado.

| **Type**  | **Topic**  | **Payload**  |
|--- |:---: |:---: |
| *COMMAND*  | /area/<span style="color: royalblue">:area</span>/relay/<span style="color: red">off</span>/ok  | <span style="color: yellowgreen">{data}</span>  |

| **Type**  | **Params**  | **Value**  | **Description**  |
|--- |:---: |:---: |--- |
| *TOPIC_PARAM*  | <span style="color: royalblue">area</span>  | <span style="color: tan">Integer</span>  | Código identificativo de la zona a la que pertenece el actuador.  |
| *PAYLOAD*  | <span style="color: yellowgreen">data</span>  | <span style="color: tan">JSON</span>  | Datos (actualmente vacío)  |

**estado:**

```json
{}
```
