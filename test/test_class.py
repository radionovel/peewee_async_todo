import pytest

from object_test_class import ObjectTestClass
from repository import ItemsRepository


@pytest.mark.asyncio
class TestClass(ObjectTestClass):

    async def test_startup(self):
        repos = ItemsRepository()
        items = await repos.list()
        assert 1 == 1

    async def test_startup2(self):
        repos = ItemsRepository()
        items = await repos.list()
        assert 1 == 1
