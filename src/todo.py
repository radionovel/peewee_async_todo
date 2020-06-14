from playhouse.shortcuts import model_to_dict

from database import TodoItem, objects, TodoTags, Tags


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

    @staticmethod
    async def get(todo_id: int):
        query = (TodoItem.select().where(TodoItem.id == todo_id))
        todo = await objects.get(query)
        return model_to_dict(todo, recurse=False)

    def build_filter(self, query):
        for (k, v) in self.filter.items():
            query = query.where(v)
        return query

    async def add(self, data: dict):
        todo = await objects.create(TodoItem, **data)
        return model_to_dict(todo, recurse=False)


class TagsRepository:

    @staticmethod
    async def get_or_create(tag_name):
        data = {
            'name': tag_name
        }
        tag, is_created = await objects.get_or_create(Tags, **data)
        return model_to_dict(tag, recurse=False)

    async def all(self):
        pass

    async def get(self, tag_name):
        pass


class TodoTagsRepository:
    def __init__(self, **kwargs):
        self.tags_repository = TagsRepository()
        self.todo_id = None
        self.for_(**kwargs)

    def for_(self, todo: dict = None, todo_id: int = 0):
        """
        Set TodoItem
        :param todo:
        :param todo_id:
        :return:
        """
        if todo and todo.get('id', None):
            self.todo_id = todo.get('id')
        elif todo_id:
            self.todo_id = todo_id
        return self

    async def _create(self, tag_id: int):
        data = {
            'tag': tag_id,
            'todo': self.todo_id
        }
        tag, is_created = await objects.get_or_create(TodoTags, **data)
        return tag

    async def _add_tag(self, tag_name):
        """
        Add tag to for TodoItem
        :param tag_name:
        :return:
        """
        tag = await self.tags_repository.get_or_create(tag_name)
        await self._create(tag_id=tag['id'])

    async def assign_tags(self, tags: list):
        """
        Assign Tags list for TodoItem
        :param tags:
        :return:
        """
        if not self.todo_id:
            raise RuntimeError('Unknown todo item')

        await self._clear_todo_tags()
        for tag_name in tags:
            await self._add_tag(tag_name)

    async def _clear_todo_tags(self):
        """
        Clear all current tags for TodoItem
        :return:
        """
        await objects.execute((TodoTags.delete().where(TodoTags.todo == self.todo_id)))
