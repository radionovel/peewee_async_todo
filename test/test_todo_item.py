import random

import pytest
from faker import Faker
from playhouse.shortcuts import model_to_dict

from database import TodoItem, objects
from object_test_class import ObjectTestClass
from todo import TodoRepository, TodoTagsRepository

fake = Faker(['ru_RU'])


class TodoHelper:

    @classmethod
    def make_todo_item_data(cls, is_completed):
        return {
            'title': fake.text(50),
            'description': fake.text(200),
            'is_completed': is_completed if is_completed is not None else bool(random.randint(0, 1))
        }

    @classmethod
    async def generate_todo_item(cls, is_completed=None):
        data = cls.make_todo_item_data(is_completed)
        todo = await objects.create(TodoItem, **data)
        return model_to_dict(todo, recurse=False)

    @classmethod
    async def generate_todo_list(cls, count, is_completed=None):
        result = []
        while count > 0:
            count -= 1
            todo = await cls.generate_todo_item(is_completed)
            result.append(todo)


@pytest.mark.asyncio
class TestTodoItem(ObjectTestClass):

    def setup_method(self, method):
        super().setup_method(method)

    @staticmethod
    def get_todo_repository():
        return TodoRepository()

    async def test_create_one(self):
        data = TodoHelper.make_todo_item_data(False)
        todo = await self.get_todo_repository().add(data)
        assert isinstance(todo, dict), 'Должен быть словарь'
        assert todo.get('is_completed') == data['is_completed']
        assert todo.get('title') == data['title']
        assert todo.get('description') == data['description']
        assert todo.get('created_at') is not None
        assert todo.get('completed_at') is None

    async def test_get_list(self):
        await TodoHelper.generate_todo_list(10)
        items = await self.get_todo_repository().list()
        assert isinstance(items, list) is True, 'Не является списком'


@pytest.mark.asyncio
class TestTodoTagsRepositoryAssigner(ObjectTestClass):

    async def test_create_assigner_with_dict(self):
        todo_item = await TodoHelper.generate_todo_item(False)

        assigner = TodoTagsRepository(todo=todo_item)
        assert assigner.todo_id == todo_item['id']

        assigner = TodoTagsRepository()
        assigner.for_(todo=todo_item)
        assert assigner.todo_id == todo_item['id']

    async def test_create_assigner_with_id(self):
        todo_item = await TodoHelper.generate_todo_item(False)
        
        assigner = TodoTagsRepository(todo_id=todo_item['id'])
        assert assigner.todo_id == todo_item['id']

        assigner = TodoTagsRepository()
        assigner.for_(todo_id=todo_item['id'])
        assert assigner.todo_id == todo_item['id']

    async def test_error_with_unknown_task(self):
        with pytest.raises(RuntimeError) as exception:
            await TodoTagsRepository().assign_tags([])
            assert str(exception) == 'Unknown todo item'

    async def test_assign_tags(self):
        todo_item = await TodoHelper.generate_todo_item(False)
        assigner = TodoTagsRepository(todo=todo_item)

        await assigner.assign_tags(['tag1', 'tag2', 'tag3'])
        todo = await objects.get(TodoItem, id=todo_item['id'])
        assert len(todo.tags) == 3

        await assigner.assign_tags(['tag5', 'tag6', 'tag7'])
        todo = await objects.get(TodoItem, id=todo_item['id'])
        assert len(todo.tags) == 3
