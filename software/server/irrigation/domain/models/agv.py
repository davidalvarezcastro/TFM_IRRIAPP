# -*- coding: utf-8 -*-
import attr

BATERIA_BAJA = 25
ESTADO_AGV_APAGADO = 0
ESTADO_AGV_OPERATIVO = 1
ESTADO_AGV_RECARGANDO = 2

@attr.s
class AgvSGA():
    """ Clase que define el modelo del AGV del SGA """
    agv: int = attr.ib()
    almacen: int = attr.ib()
    ip: int = attr.ib()
    descripcion: str = attr.ib()
    estado_agv: int = attr.ib()
    estado: int = attr.ib()
    ciclo: int = attr.ib()
    bateria: float = attr.ib()

    # METHODS
    def agv_apagado(self) -> bool:
        return self.estado_agv == ESTADO_AGV_APAGADO

    def agv_operativo(self) -> bool:
        return self.estado_agv == ESTADO_AGV_OPERATIVO

    def agv_recargando(self) -> bool:
        return self.estado_agv == ESTADO_AGV_RECARGANDO

    def bateria_baja(self) -> bool:
        return self.bateria < BATERIA_BAJA
