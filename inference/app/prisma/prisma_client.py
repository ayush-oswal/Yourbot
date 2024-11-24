from prisma import Prisma

class PrismaClient:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    async def initialize(self):
        if not self._initialized:
            self.client = Prisma()
            await self.client.connect()
            self._initialized = True
        return self.client

prisma_client = PrismaClient()

# Export the async getter function
async def get_prisma():
    return await prisma_client.initialize()