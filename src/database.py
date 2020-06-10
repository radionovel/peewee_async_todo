import peewee
import peewee_async

config = {
    'host': 'localhost',
    'port': 33006,
    'database': 'app',
    'user': 'root',
    'password': 'secret'
}

#
# class PeeweeWrapper:
#
#     db = None
#
#     def __init__(self):
#         self.db = peewee_async.PooledMySQLDatabase(**config)
#
#     def __getattr__(self, item):
#         manager = peewee_async.Manager(database=self.db)
#         return getattr(manager, item)

database_proxy = peewee.DatabaseProxy()
# ebjects = PeeweeWrapper()
database = peewee_async.PooledMySQLDatabase(**config)
# database_proxy.initialize(database)
objects = peewee_async.Manager(database=database)


class Items(peewee.Model):
    name = peewee.CharField()

    class Meta:
        database = database
        # database = ebjects.db
