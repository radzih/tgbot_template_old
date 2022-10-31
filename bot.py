import sys
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from tgbot.misc.setup_django import setup_django; setup_django()
from tgbot.filters.admin import AdminFilter
from tgbot.config import load_config, Config
from tgbot.handlers.start import register_start_handlers
from tgbot.handlers.errors import register_error_handlers
from tgbot.middlewares.environment import EnvironmentMiddleware

logger = logging.getLogger(__name__)


def register_all_middlewares(
    dp: Dispatcher, 
    config: Config,
    storage: RedisStorage2 | MemoryStorage,
    scheduler: AsyncIOScheduler,
    ):
    dp.setup_middleware(
        EnvironmentMiddleware(
            config=config,
            dp=dp,
            storage=storage,
            scheduler=scheduler,
        )
    )

def register_all_filters(dp: Dispatcher):
    dp.filters_factory.bind(AdminFilter)


def register_all_handlers(dp: Dispatcher):
    register_start_handlers(dp)
    register_error_handlers(dp)


async def main():
    formatter = logging.Formatter(
        fmt=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
        datefmt="%H:%M:%S"
    )
    logging.basicConfig(
        level=logging.INFO,
        format=formatter._fmt,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('log/bot/bot.log'),
        ]
    )

    logger.info("Starting bot")
    config = load_config(".env")

    scheduler = AsyncIOScheduler()
    storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)

    bot['config'] = config

    register_all_middlewares(dp, config, storage, scheduler)
    register_all_filters(dp)
    register_all_handlers(dp)

    # start
    try:
        scheduler.start()
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
