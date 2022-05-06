from aiogram import Dispatcher
from aiogram import types
from tgbot.services import hentai_lib
from aiogram.types.inline_query_result import InlineQueryResultArticle


async def inline_search(query: types.InlineQuery):
    results = []
    request = query.query.lower()
    if query.query == "🔥":
        response = hentai_lib.get_most_popular_list()
    else:
        response = hentai_lib.search_doujin(request)
    for i in range(len(response)):
        results.append(
            InlineQueryResultArticle(
                id=str(i + 1),
                title=response[i]["title"]["english"],
                input_message_content=types.InputMessageContent(
                    message_text=f'{response[i]["id"]}'),
                thumb_url=response[i]["cover"]["src"], thumb_width=48, thumb_height=48

            )
        )
    await query.answer(results, cache_time=120)


def register_inline_user(dp: Dispatcher):
    dp.register_inline_handler(inline_search, lambda query: len(query.query) > 0, state="*")

