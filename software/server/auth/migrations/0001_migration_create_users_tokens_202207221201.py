# auto-generated snapshot
from peewee import AutoField, CharField, BooleanField, \
    DateTimeField, SQL, Model

snapshot = Snapshot()


@snapshot.append
class Usuarios(Model):
    id_user = AutoField(primary_key=True)
    username = CharField(max_length=50, unique=True)
    password = CharField(max_length=128)
    email = CharField(max_length=250, unique=True)
    es_admin = BooleanField(constraints=[SQL("DEFAULT '0'")])
    activo = BooleanField(constraints=[SQL("DEFAULT '0'")])
    salt = CharField(max_length=50, null=True)

    class Meta:
        table_name = "usuarios"


@snapshot.append
class Tokens(Model):
    id_token = AutoField(primary_key=True)
    token = CharField(constraints=[SQL("DEFAULT '0'")], max_length=300, null=True)
    id_user = snapshot.ForeignKeyField(
        column_name='id_user', constraints=[SQL('DEFAULT 0')],
        index=True, model='usuarios', null=True)
    date = DateTimeField(constraints=[SQL('DEFAULT current_timestamp()')])

    class Meta:
        table_name = "tokens"
