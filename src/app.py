import peewee_async

config = {
    'host': 'localhost',
    'port': '33006',
    'database': 'app',
    'user': 'root',
    'password': 'secret'
}

db = peewee_async.PooledMySQLDatabase(config)

manager = peewee_async.Manager(database=db)

print(manager)
