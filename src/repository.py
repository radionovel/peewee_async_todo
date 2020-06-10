from database import Items, objects


class ItemsRepository():
    async def list(self):
        query = (Items.select())
        return await objects.execute(query)

    async def get(self, id):
        query = (Items.select().where(Items.id == id))
        return await objects.get(query)
