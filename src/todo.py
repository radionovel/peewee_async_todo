from playhouse.shortcuts import model_to_dict

from database import TodoItem, objects


class TodoRepository:

    def __init__(self):
        self.filter = {}

    def active(self):
        self.filter['is_completed'] = (TodoItem.is_completed == False)
        return self

    async def list(self):
        query = (TodoItem.select())
        query = self.build_filter(query)
        items = await objects.execute(query)
        return [model_to_dict(todo, recurse=False) for todo in items]

    async def get(self, id):
        query = (TodoItem.select().where(TodoItem.id == id))
        todo = await objects.get(query)
        return model_to_dict(todo, recurse=False)

    def build_filter(self, query):
        for (k, v) in self.filter.items():
            query = query.where(v)
        return query
