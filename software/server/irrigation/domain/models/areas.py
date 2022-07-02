# -*- coding: utf-8 -*-
from datetime import datetime
import attr


@attr.s
class Area():
    id: int = attr.ib()
    name: str = attr.ib()
    description: str = attr.ib(default=None)
    visible: bool = attr.ib(default=True)
    date: datetime = attr.ib(default=None)
