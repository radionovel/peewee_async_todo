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


class BaseModel(peewee.Model):
    class Meta:
        database = database


class Tags(BaseModel):
    name = peewee.CharField(max_length=50)

    class Meta:
        database = database


class TodoItem(BaseModel):
    title = peewee.CharField(null=False)
    description = peewee.TextField()
    is_completed = peewee.BooleanField(default=False, null=False)
    created_at = peewee.DateTimeField(default=datetime.now, null=False)
    completed_at = peewee.DateTimeField(default=None)
    overdue_at = peewee.DateTimeField(default=None)


class TodoTags(BaseModel):
    todo = peewee.ForeignKeyField(TodoItem, backref='tags')
    tag = peewee.ForeignKeyField(Tags, backref='todos')
