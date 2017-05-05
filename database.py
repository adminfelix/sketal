import peewee
import peewee_async

from settings import DATABASE_SETTINGS

if len(DATABASE_SETTINGS) == 0:
    database = False
elif len(DATABASE_SETTINGS) == 1:
    name, = DATABASE_SETTINGS
    database = peewee_async.PostgresqlDatabase(name)
else:
    name, host, port, user, password = DATABASE_SETTINGS
    database = peewee_async.PostgresqlDatabase(name,
                                               host=host,
                                               port=port,
                                               user=user,
                                               password=password)


async def get_or_none(model, *args, **kwargs):
    try:
        return await db.get(model, *args, **kwargs)

    except peewee.DoesNotExist:
        return None


class BaseModel(peewee.Model):
    class Meta:
        database = database


class User(BaseModel):
    uid = peewee.BigIntegerField(primary_key=True, unique=True)
    message_date = peewee.BigIntegerField(default=0)

    do_not_disturb = peewee.BooleanField(default=False)
    memory = peewee.TextField(default="")


class Ignore(BaseModel):
    ignored = peewee.ForeignKeyField(User, related_name='ignored_by')
    ignored_by = peewee.ForeignKeyField(User, related_name='ignored')

    class Meta:
        indexes = (
            (('ignored', 'ignored_by'), True),
        )

if database:
    db = peewee_async.Manager(database)

    User.create_table(True)
    Ignore.create_table(True)

else:
    from fake_database import *