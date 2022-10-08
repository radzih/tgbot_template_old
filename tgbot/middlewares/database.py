from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.asyncio.session import AsyncSession
from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware


class DatabaseMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ["error", "update"]

    def __init__(self, session_pool: sessionmaker):
        super().__init__()
        self.session_pool = session_pool

    async def pre_process(self, obj, data, *args):
        session = self.session_pool()

        data['session'] = session

    async def post_process(self, obj, data, *args):
        session: AsyncSession = data['session']
        await session.close()
