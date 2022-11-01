import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.types import BotCommand

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from sqlalchemy.orm import sessionmaker

from tgbot.config import Config, load_config
from tgbot.filters.admin import AdminFilter
from tgbot.infrastucture.database.functions.setup import create_session_pool
from tgbot.middlewares.database import DatabaseMiddleware
from tgbot.middlewares.environment import EnvironmentMiddleware

logger = logging.getLogger(__name__)


def register_all_middlewares(
    dp: Dispatcher,
    config: Config,
    storage: RedisStorage2 | MemoryStorage,
    scheduler: AsyncIOScheduler,
    session_pool: sessionmaker,
):
    dp.setup_middleware(
        EnvironmentMiddleware(
            config=config,
            dp=dp,
            storage=storage,
            scheduler=scheduler,
        )
    )
    dp.setup_middleware(
        DatabaseMiddleware(
            session_pool=session_pool,
        )
    )


def register_all_filters(dp: Dispatcher):
    dp.filters_factory.bind(AdminFilter)


def register_all_handlers(dp: Dispatcher):
    pass


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=(
            u'%(filename)s:%(lineno)d #%(levelname)-8s '
            u'[%(asctime)s] - %(name)s - %(message)s'
        ),
        datefmt='%H:%M:%S',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('log/bot/bot.log'),
        ]
    )

    logger.info('Starting bot')
    config = load_config('.env')

    scheduler = AsyncIOScheduler()
    storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)
    session_pool = create_session_pool(config.db)

    bot['config'] = config

    register_all_middlewares(dp, config, storage, scheduler, session_pool)
    register_all_filters(dp)
    register_all_handlers(dp)

    # start
    try:
        scheduler.start()
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close() if bot.session else None
        scheduler.shutdown()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error('Bot stopped!')
