# -*- coding: utf-8 -*-
import attr


@attr.s
class AreaType():
    description: str = attr.ib()
    id: int = attr.ib(default=-1)
