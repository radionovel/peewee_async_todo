import pytest

from object_test_class import ObjectTestClass
from todo import TodoRepository


class TodosHelper:
    @staticmethod
    async def generate_todo_item(is_completed=None):
        pass

    @staticmethod
    async def generate_todo_list(count, is_completed=None):
        pass


@pytest.mark.asyncio
class TestTodoItem(ObjectTestClass):

    def __init__(self):
        super().__init__()
        self.repository = TodoRepository()

    def setup_method(self, method):
        super().setup_method(method)
        self.repository = TodoRepository()

    async def test_get_list(self, todos):
        await TodosHelper.generate_todo_list(10)
        items = self.repository.list()
        assert isinstance(items, list) is True
        assert len(items) == 10
