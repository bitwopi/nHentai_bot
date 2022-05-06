from aiogram.dispatcher.filters.state import State, StatesGroup


class ChoosePopular(StatesGroup):
    waiting_for_number = State()


class SearchTitle(StatesGroup):
    waiting_for_name = State()
    waiting_for_number = State()


class SearchByID(StatesGroup):
    waiting_for_action = State()
