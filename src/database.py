from datetime import datetime

import peewee
import peewee_async

config = {
    'host': 'localhost',
    'port': 33006,
    'database': 'app',
    'user': 'root',
    'password': 'secret'
}

database = peewee_async.PooledMySQLDatabase(**config)
# database_proxy = peewee.DatabaseProxy()
# database_proxy.initialize(database)
objects = peewee_async.Manager(database=database)


class TodoItem(peewee.Model):

    title = peewee.CharField(null=False)
    is_completed = peewee.BooleanField(default=False, null=False)
    created_at = peewee.DateTimeField(default=datetime.now, null=False)
    completed_at = peewee.DateTimeField(default=None)

    class Meta:
        database = database
