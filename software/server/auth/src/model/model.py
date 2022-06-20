# -*- coding: utf-8 -*-
""" Modelos de la aplicación del Control de Flota
"""
from peewee import MySQLDatabase, AutoField, CharField, BooleanField, \
                   ForeignKeyField, DateTimeField, SQL, Model
from src.config import db_settings

database = MySQLDatabase(db_settings.DATABASE, **{
    'charset': 'utf8', 'sql_mode': 'PIPES_AS_CONCAT',
    'use_unicode': True, 'host': db_settings.HOST,
    'port': db_settings.PORT, 'user': db_settings.USER,
    'password': db_settings.PASSWORD})


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = database


class Usuarios(BaseModel):
    id_user = AutoField()
    email = CharField(250, unique=True)
    username = CharField(50, unique=True)
    password = CharField(128)
    es_admin = BooleanField(constraints=[SQL("DEFAULT '0'")])
    activo = BooleanField(constraints=[SQL("DEFAULT '0'")])
    salt = CharField(50, null=True)

    class Meta:
        table_name = 'usuarios'


class Tokens(BaseModel):
    id_token = AutoField()
    token = CharField(300, constraints=[SQL("DEFAULT '0'")], null=True)
    id_user = ForeignKeyField(column_name='id_user', constraints=[SQL(
        "DEFAULT 0")], field='id_user', model=Usuarios, null=True)
    date = DateTimeField(constraints=[SQL("DEFAULT current_timestamp()")])

    class Meta:
        table_name = 'tokens'
