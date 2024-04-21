import asyncio
import logging
from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage


def ikb(name, df):
    return InlineKeyboardButton(text=name, callback_data=df)


menus = [
    [ikb("Добавить домашнее задание", "set_hw"),
     ikb("Получить домашнее задание", "get_hw")],
    [ikb("Расписание", "rasp")],
    [ikb("Режим админа", "admin")]
]

dates = [
    [ikb("Понедельник", "pn")],
    [ikb("Вторник", "vt")],
    [ikb("Среда", "sr")],
    [ikb("Четверг", "ct")],
    [ikb("Пятница", "pt")],
    [ikb("Суббота", "sb")],
    [ikb("Воскресение", "vs")],
    [ikb('Следющая неделя', "next_week")],
    [ikb('Отмена', 'menu')]
]

chooses = [
    [ikb('Текст', 'txt'), ikb("фото", "photo")],
    [ikb('Отмена', 'menu')]
]

ends = [[ikb('Отмена', 'menu')]]

yep = ["pn", "vt", "sr", "ct", "pt", "sb", "vs"]

men = InlineKeyboardMarkup(inline_keyboard=menus)
date = InlineKeyboardMarkup(inline_keyboard=dates)
choose = InlineKeyboardMarkup(inline_keyboard=chooses)
end = InlineKeyboardMarkup(inline_keyboard=ends)

greet_text = "Приветствую, {name}, это бот для школ \n \nУдачного использования"
menu_text = "Функции"
set_date_text = "Выберите день недели"
choose_how = "Выберите вид домашнего задания"
set_hw_text = 'Впишите ваше домашнее задание'
set_hw_photo = 'Вставте фото вашего домашнего задания'

router = Router()


@router.callback_query(F.data == 'set_hw')
async def set_date(call: types.CallbackQuery):
    await call.message.answer(set_date_text, reply_markup=date)

for i in yep:
    @router.callback_query(F.data == i)
    async def choose_hw(call: types.CallbackQuery):
        day = i
        await call.message.answer(choose_how, reply_markup=choose)


@router.callback_query(F.data == 'txt')
async def set_hw(call: types.CallbackQuery):
    await call.message.answer(set_hw_text, reply_markup=end)


@router.callback_query(F.data == 'photo')
async def set_hw(call: types.CallbackQuery):
    await call.message.answer(set_hw_photo, reply_markup=end)


@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer(greet_text.format(name=msg.from_user.full_name), reply_markup=men)


@router.message(F.text.lower() == "меню")
@router.message(Command('menu'))
async def menu(msg: Message):
    await msg.answer(menu_text, reply_markup=men)


@router.callback_query(F.data == 'menu')
async def menu(call: types.CallbackQuery):
    await call.message.answer(menu_text, reply_markup=men)


async def main():
    bot = Bot(token="7087953766:AAHZhEaNOHUwuVr-49sizlgdCG-i7LgZz3w", parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
