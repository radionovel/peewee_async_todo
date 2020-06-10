import asyncio

import peewee_async
import pytest

from database import Items, config, database, database_proxy
from repository import ItemsRepository


def init_database():
    database.init(**config)
    database.objects = peewee_async.Manager(database=database)


def setup_module():
    init_database()
    database.create_tables(models=[Items])


def teardown_module():
    database.drop_tables(models=[Items])


def setup_function():
    init_database()


def teardown_function():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(database.objects.close())
    loop.close()


@pytest.mark.asyncio
async def test_test1():
    repos = ItemsRepository()
    items = await repos.list()
    assert 1 == 1


@pytest.mark.asyncio
async def test_test2(event_loop):
    repos = ItemsRepository()
    await repos.list()
    assert 1 == 1
