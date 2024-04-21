import asyncio
import logging
from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage


def IKB(name, df):
    return InlineKeyboardButton(text=name, callback_data=df)


menus = [
    [IKB("Добавить домашнее задание", "set_hw"),
     IKB("Получить домашнее задание", "get_hw")],
    [IKB("Расписание", "rasp")],
    [IKB("Режим админа", "admin")]
]

dates = [
    [IKB("Понедельник", "pn")],
    [IKB("Вторник", "vt")],
    [IKB("Среда", "sr")],
    [IKB("Четверг", "ct")],
    [IKB("Пятница", "pt")],
    [IKB("Суббота", "sb")],
    [IKB("Воскресение", "vs")],
    [IKB('Следющая неделя', "next_week")]
]

chooses = [[IKB('Текст', 'txt'), IKB("фото", "ft")]]

yep = ["pn", "vt", "sr", "ct", "pt", "sb", "vs"]

men = InlineKeyboardMarkup(inline_keyboard=menus)
date = InlineKeyboardMarkup(inline_keyboard=dates)
choose = InlineKeyboardMarkup(inline_keyboard=chooses)

greet_text = "Приветствую, {name}, это бот для школ \n \nУдачного использования"
menu_text = "Функции"
set_date_text = "Выберите день недели"
choose_how = "Выберите вид домашнего задания"
set_hw_text = 'Впишите ваше домашнее задание'

router = Router()


@router.callback_query(F.data == 'set_hw')
async def set_date(call: types.CallbackQuery):
    await call.message.answer(set_date_text, reply_markup=date)

for i in yep:
    @router.callback_query(F.data == i)
    async def set_hw(call: types.CallbackQuery):
        date1 = i
        await call.message.answer(choose_how, reply_markup=)


@router.callback_query(F.data == 'txt')



@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer(greet_text.format(name=msg.from_user.full_name), reply_markup=men)


@router.message(F.text.lower() == "меню")
@router.message(Command('menu'))
async def menu(msg: Message):
    await msg.answer(menu_text, reply_markup=men)


async def main():
    bot = Bot(token="7087953766:AAHZhEaNOHUwuVr-49sizlgdCG-i7LgZz3w", parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
