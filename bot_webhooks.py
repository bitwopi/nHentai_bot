import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.executor import start_webhook

from tgbot.config import load_config
from tgbot.filters.admin import AdminFilter
from tgbot.handlers.admin import register_admin
from tgbot.handlers.echo import register_echo
from tgbot.handlers.user import register_user
from tgbot.middlewares.db import DbMiddleware
from tgbot.services.set_bot_commands import set_default_commands
from tgbot.handlers.user_inline import register_inline_user

logger = logging.getLogger(__name__)
storage = MemoryStorage()
config = load_config(".env")
token = config.tg_bot.token
bot = Bot(token, parse_mode='HTML')
dp = Dispatcher(bot, storage=storage)
heroku_app_name = config.heroku.app_name

# webhook settings
WEBHOOK_HOST = f'https://{heroku_app_name}.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{token}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

# webserver settings
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = 8000


def register_all_middlewares(dp):
    dp.setup_middleware(DbMiddleware())


def register_all_filters(dp):
    dp.filters_factory.bind(AdminFilter)


def register_all_handlers(dp):
    register_admin(dp)
    register_user(dp)
    #register_echo(dp)
    register_inline_user(dp)


async def set_bot_commands(bot: Bot):
    await set_default_commands(bot)


async def on_startup(dispatcher):
    register_all_middlewares(dp)
    register_all_filters(dp)
    register_all_handlers(dp)
    await set_bot_commands(bot)
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)


async def on_shutdown(dispatcher):
    await bot.delete_webhook()
    await dp.storage.close()
    await dp.storage.wait_closed()
    await bot.session.close()


def main():
    logging.basicConfig(level=logging.INFO)

    bot['config'] = config
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )


if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
