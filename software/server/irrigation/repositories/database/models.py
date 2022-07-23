from sqlalchemy import Column, Integer, SmallInteger, String, Text, TIMESTAMP, \
    ForeignKey, event, text, DDL

from repositories.database.data_mysql import DATA_TYPES, DATA_AREAS, DATA_CONTROLLERS
from repositories.database.database import Base, engine


def is_sqlite() -> bool:
    return engine.dialect.name == 'sqlite'


class TypesORM(Base):
    __tablename__ = 'types'
    __table_args__ = {
        'comment':
        'table to save the different types of areas stored'}

    id = Column(Integer, primary_key=True)
    description = Column(Text)

    def __init__(self, description: str, id: int = None):
        self.id = id
        self.description = description

    def __repr__(self) -> str:
        return 'TYPE({}, {})'.format(self.id, self.description)

    def __str__(self) -> str:
        return str(self.id)

    def __dic__(self) -> dict:
        return {'id': self.id, 'description': self.description}


class AreasORM(Base):
    __tablename__ = 'areas'
    __table_args__ = {
        'comment':
        'table to save different areas'}

    id = Column(Integer, primary_key=True)
    name = Column(String(25), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    visible = Column(SmallInteger, server_default="1")
    type = Column(Integer, ForeignKey('types.id', ondelete='CASCADE', onupdate='CASCADE'), server_default="1")
    date = Column(TIMESTAMP, nullable=False,
                  server_default=text("current_timestamp()" if not is_sqlite() else "current_timestamp"))

    def __init__(
            self, name: str, type: int = 1, description: str = None, visible: bool = False, date: str = None,
            id: int = None):
        self.id = id
        self.type = type
        self.name = name
        self.description = description
        self.visible = visible

    def __repr__(self) -> str:
        return 'Area ({}, {})'.format(self.id, self.name)

    def __str__(self) -> str:
        return str(self.name)

    def __dic__(self) -> dict:
        return {
            'id': self.id,
            'type': self.type,
            'name': self.name,
            'description': self.description,
            'visible': self.visible,
            'date': self.date,
        }


class ControllersORM(Base):
    __tablename__ = 'controllers'
    __table_args__ = {
        'comment':
        'table to save the controller set from a specific area'}

    id = Column(Integer, primary_key=True)
    area = Column(Integer, ForeignKey('areas.id', ondelete='CASCADE', onupdate='CASCADE'))
    name = Column(String(25), nullable=False)
    description = Column(Text, nullable=True)
    key = Column(String(128), nullable=True)
    visible = Column(SmallInteger, server_default="1")
    date = Column(TIMESTAMP, nullable=False,
                  server_default=text("current_timestamp()" if not is_sqlite() else "current_timestamp"))

    def __init__(
            self, area: int, name: str, description: str = None, key: str = None, visible: bool = False,
            date: str = None, id: int = None):
        self.area = area
        self.id = id
        self.name = name
        self.description = description
        self.key = key
        self.visible = visible

    def __repr__(self) -> str:
        return 'Controller ({}-{}, {})'.format(self.area, self.id, self.name)

    def __str__(self) -> str:
        return str(self.name)

    def __dic__(self) -> dict:
        return {
            'area': self.area,
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'key': self.description,
            'visible': self.visible,
            'date': self.date,
        }


# TRIGGERS
trigger_update_visible = DDL("CREATE TRIGGER area_update_visibility \
        AFTER UPDATE ON areas \
        FOR EACH ROW \
    BEGIN \
        UPDATE controllers SET visible = NEW.visible  \
        WHERE area = NEW.id; \
END;")


# EVENTS
def insert_area_types(target, connection, **kw):
    connection.execute(target.insert(), DATA_TYPES)


def insert_areas(target, connection, **kw):
    connection.execute(target.insert(), DATA_AREAS)


def insert_controllers(target, connection, **kw):
    connection.execute(target.insert(), DATA_CONTROLLERS)


event.listen(TypesORM.__table__, 'after_create', insert_area_types)
event.listen(AreasORM.__table__, 'after_create', insert_areas)
event.listen(ControllersORM.__table__, 'after_create', insert_controllers)

event.listen(
    AreasORM.__table__,
    "after_create",
    trigger_update_visible.execute_if(dialect=('postgresql', 'mysql'))
)

# tables creation
Base.metadata.create_all(bind=engine)
