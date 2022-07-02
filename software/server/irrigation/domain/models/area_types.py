# -*- coding: utf-8 -*-
import attr


@attr.s
class AreaType():
    id: int = attr.ib()
    description: str = attr.ib(default=None)
