import asyncio
import logging
from aiogram import F, Router
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
men = InlineKeyboardMarkup(inline_keyboard=menus)

greet_text = "Приветствую, {name}, это бот для школ \n \nУдачного использования"
menu_text = "Функции"

router = Router()


@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer(greet_text.format(name=msg.from_user.full_name), reply_markup=men)


@router.message(F.text.lower() == "меню")
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
