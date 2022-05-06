from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_default_commands(bot: Bot):
    return await bot.set_my_commands(
        commands=[
            BotCommand('start', 'start your communication with bot'),
            BotCommand('help', 'show all useful bot commands'),
            BotCommand('search', 'search doujins by name')
        ],
        scope=BotCommandScopeDefault()
    )
