# -*- coding: utf-8 -*-
import marshmallow as ma


class SchemaAgvSGA(ma.Schema):
    """Schema AGV SGA_AGVS
    """
    COD_AGV = ma.fields.Integer(\
      data_key='agv',\
      error_messages={\
        'invalid': 'El campo `COD_AGV` solo admite valores de tipo Integer.'\
    })
    COD_ALMACEN = ma.fields.Integer(\
      data_key='almacen',\
      error_messages={\
        'invalid': 'El campo `COD_ALMACEN` solo admite valores de tipo Integer.'\
    })
    IP = ma.fields.Str(\
      data_key='ip',\
      error_messages={\
        'invalid': 'El campo `IP` solo admite valores de tipo String.'\
    })
    DESCRI = ma.fields.Str(\
      data_key='descripcion',\
      error_messages={\
        'invalid': 'El campo `DESCRI` solo admite valores de tipo String.'\
    })
    ESTADO_AGV = ma.fields.Integer(\
      data_key='estado_agv',\
      error_messages={\
        'invalid': 'El campo `ESTADO_AGV` solo admite valores de tipo Integer.'\
    })
    ESTADO = ma.fields.Integer(\
      data_key='estado',\
      error_messages={\
        'invalid': 'El campo `ESTADO` solo admite valores de tipo Integer.'\
    })
    CICLO_CARGA = ma.fields.Integer(\
      data_key='ciclo',\
      error_messages={\
        'invalid': 'El campo `CICLO_CARGA` solo admite valores de tipo Integer.'\
    })
    BATERIA = ma.fields.Float(\
      data_key='bateria',\
      error_messages={\
        'invalid': 'El campo `BATERIA` solo admite valores de tipo Integer.'\
    })
