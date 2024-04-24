import asyncio
import logging
from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

day = None
work = None
night = None


class States(StatesGroup):
    txt = State()
    photo = State()
    none = State()


def ikb(name, df):
    return InlineKeyboardButton(text=name, callback_data=df)


menus = [
    [ikb("Добавить домашнее задание", "set_hw"),
     ikb("Получить домашнее задание", "get_hw")],
    [ikb("Расписание", "rasp")],
    [ikb("Режим админа", "admin")]
]


weeks = [
    [ikb('Эта неделя', 'this_week'), ikb('Следющая неделя', "next_week")],
         [ikb('Отмена', 'menu')]
]


dates = [
    [ikb("Понедельник", "pn")],
    [ikb("Вторник", "vt")],
    [ikb("Среда", "sr")],
    [ikb("Четверг", "ct")],
    [ikb("Пятница", "pt")],
    [ikb("Суббота", "sb")],
    [ikb("Воскресение", "vs")],
    [ikb('Отмена', 'menu')]
]

lessons = [
    [ikb("Алгебра", 'alg'), ikb("Геометрия", 'geom'), ikb('Математика', 'mat')],
    [ikb("Физика", 'phy'), ikb("Химия", 'che')],
    [ikb("Информатика", 'IT'), ikb("Иностранный язык", 'eng')],
    [ikb("Русский", 'rus'), ikb("Литература", 'lit')],
    [ikb("История", 'his'), ikb("Обществознание", 'cit')],
    [ikb("География", 'geog'), ikb("Биология", 'bio')],
    [ikb("Физкультура", 'PE'), ikb("ОБЖ", 'ob')],
    [ikb("ИЗО", 'izo'), ikb("Труды", 'tru'), ikb("Музыка", 'mus')],
    [ikb("Разговоры о важном", 'rov')],
    [ikb("Отмена", 'menu')]
]

chooses = [
    [ikb('Текст', 'txt'), ikb("фото", "photo")],
    [ikb('Отмена', 'menu')]
]

ends = [[ikb('Отмена', 'menu')]]

yep = {"pn": 'Понедельник', "vt": 'Вторник', "sr": 'Среда', "ct": 'Четверг',
       "pt": 'Пятница', "sb": "Суббота", "vs": "Воскресенье"}

nope = {'alg': 'Алгебра', 'geom': 'Геометрия', 'phy': 'Физика', 'che': 'Химия', 'IT': 'Информатика',
        'eng': 'Иностранный язык', 'rus': 'Русский', 'lit': 'Литература', 'his': 'История', 'cit': 'Обществознание',
        'geog': 'География', 'bio': 'Биология', 'PE': 'Физкультура', 'ob': 'ОБЖ', 'izo': 'ИЗО', 'tru': 'Труды',
        'mus': 'Музыка', 'rov': 'Разговоры о важном', 'mat': 'Математика'}

died = {'this_week': 'этой неделе', 'next_week': 'следующей неделе'}

men = InlineKeyboardMarkup(inline_keyboard=menus)
date = InlineKeyboardMarkup(inline_keyboard=dates)
choose = InlineKeyboardMarkup(inline_keyboard=chooses)
end = InlineKeyboardMarkup(inline_keyboard=ends)
lesson = InlineKeyboardMarkup(inline_keyboard=lessons)
week = InlineKeyboardMarkup(inline_keyboard=weeks)

greet_text = "Приветствую, {name}, это бот для школ \nУдачного использования"
menu_text = "Функции"
set_date_text = "Выберите день недели"
set_lesson_text = 'Выберите предмет'
choose_how = "Выберите вид домашнего задания"
set_hw_text = 'Впишите ваше домашнее задание'
set_hw_photo = 'Вставте фото вашего домашнего задания'
set_week_text = 'Выберите неделю'

router = Router()


@router.callback_query(F.data == 'set_hw')
async def set_week(call: types.CallbackQuery):
    await call.message.answer(set_week_text, reply_markup=week)


@router.callback_query(F.data == 'this_week')
async def set_date(call: types.CallbackQuery):
    global night
    night = 'this_week'
    await call.message.answer(set_date_text, reply_markup=date)


@router.callback_query(F.data == 'next_week')
async def set_date(call: types.CallbackQuery):
    global night
    night = 'next_week'
    await call.message.answer(set_date_text, reply_markup=date)

# -----------------------------DATES--------------------------------


@router.callback_query(F.data == 'pn')
async def set_lesson(call: types.CallbackQuery):
    global day
    day = 'pn'
    await call.message.answer(set_lesson_text, reply_markup=lesson)


@router.callback_query(F.data == 'vt')
async def set_lesson(call: types.CallbackQuery):
    global day
    day = 'vt'
    await call.message.answer(set_lesson_text, reply_markup=lesson)


@router.callback_query(F.data == 'sr')
async def set_lesson(call: types.CallbackQuery):
    global day
    day = 'sr'
    await call.message.answer(set_lesson_text, reply_markup=lesson)


@router.callback_query(F.data == 'ct')
async def set_lesson(call: types.CallbackQuery):
    global day
    day = 'ct'
    await call.message.answer(set_lesson_text, reply_markup=lesson)


@router.callback_query(F.data == 'pt')
async def set_lesson(call: types.CallbackQuery):
    global day
    day = 'pt'
    await call.message.answer(set_lesson_text, reply_markup=lesson)


@router.callback_query(F.data == 'sb')
async def set_lesson(call: types.CallbackQuery):
    global day
    day = 'sb'
    await call.message.answer(set_lesson_text, reply_markup=lesson)


@router.callback_query(F.data == 'vs')
async def set_lesson(call: types.CallbackQuery):
    global day
    day = 'vs'
    await call.message.answer(set_lesson_text, reply_markup=lesson)


# -----------------------------LESSONS--------------------------------


@router.callback_query(F.data == 'alg')
async def choose_hw(call: types.CallbackQuery):
    global work
    work = 'alg'
    await call.message.answer(choose_how, reply_markup=choose)


@router.callback_query(F.data == 'geom')
async def choose_hw(call: types.CallbackQuery):
    global work
    work = 'geom'
    await call.message.answer(choose_how, reply_markup=choose)


@router.callback_query(F.data == 'mat')
async def choose_hw(call: types.CallbackQuery):
    global work
    work = 'mat'
    await call.message.answer(choose_how, reply_markup=choose)


@router.callback_query(F.data == 'phy')
async def choose_hw(call: types.CallbackQuery):
    global work
    work = 'phy'
    await call.message.answer(choose_how, reply_markup=choose)


@router.callback_query(F.data == 'che')
async def choose_hw(call: types.CallbackQuery):
    global work
    work = 'che'
    await call.message.answer(choose_how, reply_markup=choose)


@router.callback_query(F.data == 'IT')
async def choose_hw(call: types.CallbackQuery):
    global work
    work = 'IT'
    await call.message.answer(choose_how, reply_markup=choose)


@router.callback_query(F.data == 'eng')
async def choose_hw(call: types.CallbackQuery):
    global work
    work = 'eng'
    await call.message.answer(choose_how, reply_markup=choose)


@router.callback_query(F.data == 'rus')
async def choose_hw(call: types.CallbackQuery):
    global work
    work = 'rus'
    await call.message.answer(choose_how, reply_markup=choose)


@router.callback_query(F.data == 'lit')
async def choose_hw(call: types.CallbackQuery):
    global work
    work = 'lit'
    await call.message.answer(choose_how, reply_markup=choose)


@router.callback_query(F.data == 'his')
async def choose_hw(call: types.CallbackQuery):
    global work
    work = 'his'
    await call.message.answer(choose_how, reply_markup=choose)


@router.callback_query(F.data == 'cit')
async def choose_hw(call: types.CallbackQuery):
    global work
    work = 'cit'
    await call.message.answer(choose_how, reply_markup=choose)


@router.callback_query(F.data == 'geog')
async def choose_hw(call: types.CallbackQuery):
    global work
    work = 'geog'
    await call.message.answer(choose_how, reply_markup=choose)


@router.callback_query(F.data == 'bio')
async def choose_hw(call: types.CallbackQuery):
    global work
    work = 'bio'
    await call.message.answer(choose_how, reply_markup=choose)


@router.callback_query(F.data == 'PE')
async def choose_hw(call: types.CallbackQuery):
    global work
    work = 'PE'
    await call.message.answer(choose_how, reply_markup=choose)


@router.callback_query(F.data == 'ob')
async def choose_hw(call: types.CallbackQuery):
    global work
    work = 'ob'
    await call.message.answer(choose_how, reply_markup=choose)


@router.callback_query(F.data == 'izo')
async def choose_hw(call: types.CallbackQuery):
    global work
    work = 'izo'
    await call.message.answer(choose_how, reply_markup=choose)


@router.callback_query(F.data == 'tru')
async def choose_hw(call: types.CallbackQuery):
    global work
    work = 'tru'
    await call.message.answer(choose_how, reply_markup=choose)


@router.callback_query(F.data == 'mus')
async def choose_hw(call: types.CallbackQuery):
    global work
    work = 'mus'
    await call.message.answer(choose_how, reply_markup=choose)


@router.callback_query(F.data == 'rov')
async def choose_hw(call: types.CallbackQuery):
    global work
    work = 'rov'
    await call.message.answer(choose_how, reply_markup=choose)


@router.callback_query(F.data == 'txt')
async def set_hw(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(set_hw_text, reply_markup=end)
    await state.set_state(States.txt)


@router.message(States.txt)
async def text_hw(msg: Message):
    await msg.answer(f'ваша домашняя работа по {nope[work]} на {yep[day]} на {died[night]}: {msg.text}')


@router.callback_query(F.data == 'photo')
async def set_hw(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(set_hw_photo, reply_markup=end)
    await state.set_state(States.photo)


# @router.message(States.photo)
# async def text_hw(msg: Message):
#     id_photo = msg.photo[-1].file_id
#     name_photo = msg.caption
#     await msg.answer(f'ваша домашняя работа на {yep[day]}:')
#   пока не работает, в будущем постараюсь реализовать
#   стоит поторопиться


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
