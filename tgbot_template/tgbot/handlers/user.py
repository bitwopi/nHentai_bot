import asyncio

import aiogram.utils.exceptions
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram import types
from tgbot_template.tgbot.services import hentai_lib
from tgbot_template.tgbot.misc.states import SearchByID
from tgbot_template.tgbot.keyboards import reply
from aiogram.utils.markdown import hlink
from tgbot_template.tgbot.keyboards import inline


# Start communication with user
async def user_start(message: types.Message):
    text = "Hi, my dear!\nWould you like to get some doujinshi😉\nI can help you with that 😘" \
           "\nUse /help to know what i can do for you ❤"
    await message.answer(text, reply_markup=reply.get_home_reply_keyboard())


# Help command
async def user_help(message: types.Message):
    text = "\n/search - search doujinshi"
    await message.answer(text)


# Sending info-card by doujin id
async def send_id_card(message: types.Message, state: FSMContext):
    try:
        int(message.text.lower())
    except:
        await message.answer("Send me the correct id, Honey❤")
        return
    categories = []
    tags = []
    languages = []
    response = hentai_lib.get_doujin_by_id(message.text)
    title = response["title"]["english"]
    for item in response["categories"]:
        categories.append(hlink(item["name"], item["url"]))
    for item in response["tags"]:
        tags.append(hlink(item["name"], item["url"]))
    for item in response["languages"]:
        languages.append(hlink(item["name"], item["url"]))
    pages = response["total_pages"]
    await message.answer_photo(response["cover"]["src"],
                               f'{title}\nCategories: {", ".join(categories)}\nTags: {", ".join(tags)}\n'
                               f'Languages: {", ".join(languages)}'
                               f'\nPages: {pages}',
                               reply_markup=inline.get_inline_card_keyboard(response["url"], response["id"]))
    await SearchByID.waiting_for_action.set()
    await state.update_data({"id": response["id"]})


# Sending info-card of random doujin
async def send_random_card(callback: types.CallbackQuery, state: FSMContext):
    response = hentai_lib.get_douijin_random()
    categories = []
    tags = []
    languages = []
    title = response["title"]["english"]
    for item in response["categories"]:
        categories.append(hlink(item["name"], item["url"]))
    for item in response["tags"]:
        tags.append(hlink(item["name"], item["url"]))
    for item in response["languages"]:
        languages.append(hlink(item["name"], item["url"]))
    pages = response["total_pages"]
    await callback.message.answer_photo(response["cover"]["src"],
                                f'{title}\nCategories: {", ".join(categories)}\nTags: {", ".join(tags)}\n'
                                f'Languages: {", ".join(languages)}'
                                f'\nPages: {pages}',
                                reply_markup=inline.get_inline_card_keyboard(response["url"], response["id"]))
    await SearchByID.waiting_for_action.set()
    await state.set_data({"id": response["id"]})


# Send search menu (inline buttons)
async def send_search_menu(message: types.Message):
    text = "Here is some search options:"
    await message.answer(text, reply_markup=inline.get_inline_search_keyboard())


# Sending doujin images to chat
async def send_id_content(callback: types.CallbackQuery, state: FSMContext):
    try:
        data = await state.get_data()
        images = hentai_lib.get_doujin_by_id(data["id"])["images"]
        if images is not None:
            media = types.MediaGroup()
            counter = 0
            for i in range(len(images)):
                if counter == 10:
                    counter = 0
                    try:
                        await callback.message.answer_media_group(media, allow_sending_without_reply=True)
                        media = types.MediaGroup()
                    except aiogram.utils.exceptions.RetryAfter as ex:
                        await asyncio.sleep(ex.timeout)
                        continue
                    except aiogram.utils.exceptions.BadRequest:
                        await callback.message.answer("Sorry, I can't do this anymore"
                                                      ", because of telegram restrictions")
                        break
                media.attach_photo(images[i]["src"])
                counter += 1
            try:
                await callback.message.answer_media_group(media, allow_sending_without_reply=True)
            except aiogram.utils.exceptions.RetryAfter as ex:
                await asyncio.sleep(ex.timeout)
            except aiogram.utils.exceptions.BadRequest:
                await callback.message.answer("Sorry, I can't do that, because of telegram restrictions")
    finally:
        await callback.message.answer("Use me more, my Dear😍", reply_markup=reply.get_home_reply_keyboard())
        await state.finish()


# Choose operation
async def choose_feature(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        if len(message.text) == 6:
            await send_id_card(message, state)
    else:
        match message.text:
            case "Search🔎":
                await send_search_menu(message)


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
    dp.register_message_handler(user_help, commands=["help"], state="*")
    dp.register_message_handler(send_search_menu, commands=["search"], state="*")
    dp.register_message_handler(choose_feature, content_types=["text"], state="*")
    dp.register_message_handler(send_id_card, state="*")
    dp.register_callback_query_handler(send_random_card, lambda cb: cb.data == "random", state="*")
    dp.register_callback_query_handler(send_id_content, lambda cb: cb.data == "images",
                                       state="SearchByID:waiting_for_action")
