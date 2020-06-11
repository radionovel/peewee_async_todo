import random

import pytest
from faker import Faker

from database import TodoItem, objects
from object_test_class import ObjectTestClass
from todo import TodoRepository

fake = Faker(['ru_RU'])


class TodoHelper:

    @classmethod
    def make_todo_item_data(cls, is_completed):
        return {
            'title': fake.text(50),
            'is_completed': is_completed if is_completed is not None else bool(random.randint(0, 1))
        }

    @classmethod
    async def generate_todo_item(cls, is_completed=None):
        data = cls.make_todo_item_data(is_completed)
        await objects.create(TodoItem, **data)

    @classmethod
    async def generate_todo_list(cls, count, is_completed=None):
        while count > 0:
            count -= 1
            await cls.generate_todo_item(is_completed)


@pytest.mark.asyncio
class TestTodoItem(ObjectTestClass):

    def setup_method(self, method):
        super().setup_method(method)
        self.repository = TodoRepository()

    async def test_create_one(self):
        data = TodoHelper.make_todo_item_data(False)
        todo = await self.repository.add(data)
        assert isinstance(todo, dict), 'Должен быть словарь'
        assert todo.get('is_completed') == data['is_completed']
        assert todo.get('title') == data['title']
        assert todo.get('created_at') is not None
        assert todo.get('completed_at') is None

    async def test_get_list(self):
        await TodoHelper.generate_todo_list(10)
        items = await self.repository.list()
        assert isinstance(items, list) is True, 'Не является списком'
