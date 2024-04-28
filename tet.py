import asyncio
import logging
from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, FSInputFile
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from data.tasks import Tasks
from data import db_session
from data.k_tables import *
from data.access import *
from data.rasp import *
from data.users import *
import datetime

router = Router()


class States(StatesGroup):
    txt = State()
    photo = State()
    none = State()
    next = State()
    true = State()


def ikb(name, df):
    return InlineKeyboardButton(text=name, callback_data=df)


day = None
work = None
night = None
admin = True
hw_id = 2

db_session.global_init("db/school_rasp.db")


menus = [
    [ikb("Добавить домашнее задание", "set_hw"),
     ikb("Получить домашнее задание", "get_hw")]
]

ads = [
    [ikb("Добавить домашнее задание", "set_hw_admin"),
     ikb("Получить домашнее задание", "get_hw")]
]

hw_types = [
    [ikb('Индивидуальная', 'ind'), ikb('Общая', 'obs')],
    [ikb('Отмена', 'menu')]
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

ends = [
    [ikb('Отмена', 'menu')]
]

yep = [
    'Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресение'
]

nope = {'alg': 'Алгебра', 'geom': 'Геометрия', 'phy': 'Физика', 'che': 'Химия', 'IT': 'Информатика',
        'eng': 'Иностранный язык', 'rus': 'Русский', 'lit': 'Литература', 'his': 'История', 'cit': 'Обществознание',
        'geog': 'География', 'bio': 'Биология', 'PE': 'Физкультура', 'ob': 'ОБЖ', 'izo': 'ИЗО', 'tru': 'Труды',
        'mus': 'Музыка', 'rov': 'Разговоры о важном', 'mat': 'Математика'}

#   ----------------------------IKBS--------------------------------
men = InlineKeyboardMarkup(inline_keyboard=menus)
date = InlineKeyboardMarkup(inline_keyboard=dates)
choose = InlineKeyboardMarkup(inline_keyboard=chooses)
end = InlineKeyboardMarkup(inline_keyboard=ends)
lesson = InlineKeyboardMarkup(inline_keyboard=lessons)
week = InlineKeyboardMarkup(inline_keyboard=weeks)
ad = InlineKeyboardMarkup(inline_keyboard=ads)
hw_type = InlineKeyboardMarkup(inline_keyboard=hw_types)

#   ---------------------------TEXTS-------------------------------
greet_text = "Приветствую, {name}, это бот для школ \nУдачного использования"
menu_text = "Функции"
set_date_text = "Выберите день недели"
set_lesson_text = 'Выберите предмет'
choose_how = "Выберите вид домашнего задания"
set_hw_text = 'Впишите ваше домашнее задание'
set_hw_photo = 'Вставте фото вашего домашнего задания'
set_week_text = 'Выберите неделю'
another_text = 'Эта дата уже прошла'
added_text = 'Ваша домашняя работа добавлена'
hw_admin_text = 'Выберите тип домашней работы'


@router.callback_query(F.data == 'set_hw_admin')
async def set_hw_admin(call: types.CallbackQuery):
    await call.message.answer(hw_admin_text, reply_markup=hw_type)


@router.callback_query(F.data == 'obs')
async def set_week(call: types.CallbackQuery):
    global hw_id
    hw_id = 1
    await call.message.answer(set_week_text, reply_markup=week)


@router.callback_query(F.data == 'ind')
async def set_week(call: types.CallbackQuery):
    global hw_id
    hw_id = 2
    await call.message.answer(set_week_text, reply_markup=week)


@router.callback_query(F.data == 'get_hw')
async def get_hw(call: types.CallbackQuery, bot: Bot):
    db_sess = db_session.create_session()
    await call.message.answer('-----------------Общая-----------------')
    klass_id = db_sess.query(User).filter(User.telegram_id == call.from_user.username).first().current_class_id
    rasps = [el.id for el in db_sess.query(Rasp).filter(Rasp.klass_id == klass_id).all()]
    for db in db_sess.query(Tasks).filter(Tasks.task_type_id == 1, Tasks.rasp_id.in_(rasps)).all():
        subj = db.rasp.subject.name
        if db.descriptions[-4:] == '.jpg':
            pht = FSInputFile(f'{db.descriptions}')
            await call.message.answer(f"{subj }:")
            await bot.send_photo(chat_id=call.message.chat.id, photo=pht)
        else:
            await call.message.answer(subj, ": ", db.descriptions)
    await call.message.answer("------------Индивидуальная------------")
    for db in db_sess.query(Tasks).filter(Tasks.task_type_id == 2, Tasks.rasp_id.in_(rasps)).all():
        if db.creator == str(call.from_user.username):
            subj = db.rasp.subject.name
            if '.jpg' in db.descriptions:
                pht = FSInputFile(f'{db.descriptions}')
                await call.message.answer(f"{subj}:")
                await bot.send_photo(chat_id=call.message.chat.id, photo=pht)
            else:
                await call.message.answer(subj + ": " + db.descriptions)
    if admin:
        await call.message.answer('Ну всё', reply_markup=ad)
    else:
        await call.message.answer('Ну всё', reply_markup=men)


@router.callback_query(F.data == 'rasp')
async def rasp(call: types.CallbackQuery):
    await call.message.answer('тут пока ничего нет')


@router.callback_query(F.data == 'set_hw')
async def set_week(call: types.CallbackQuery):
    await call.message.answer(set_week_text, reply_markup=week)


@router.callback_query(F.data == 'this_week')
async def set_date(call: types.CallbackQuery):
    global night
    night = False
    await call.message.answer(set_date_text, reply_markup=date)


@router.callback_query(F.data == 'next_week')
async def set_date(call: types.CallbackQuery):
    global night
    night = True
    await call.message.answer(set_date_text, reply_markup=date)


# -----------------------------DATES--------------------------------


@router.callback_query(F.data == 'pn')
async def set_lesson(call: types.CallbackQuery):
    global day
    now = datetime.datetime.today()
    day = 0
    if now.weekday() > day and not night:
        await call.message.answer(another_text, reply_markup=date)
    else:
        await call.message.answer(set_lesson_text, reply_markup=lesson)


@router.callback_query(F.data == 'vt')
async def set_lesson(call: types.CallbackQuery):
    global day
    now = datetime.datetime.today()
    day = 1
    if now.weekday() > day and not night:
        await call.message.answer(another_text, reply_markup=date)
    else:
        await call.message.answer(set_lesson_text, reply_markup=lesson)


@router.callback_query(F.data == 'sr')
async def set_lesson(call: types.CallbackQuery):
    global day
    now = datetime.datetime.today()
    day = 2
    if now.weekday() > day and not night:
        await call.message.answer(another_text, reply_markup=date)
    else:
        await call.message.answer(set_lesson_text, reply_markup=lesson)


@router.callback_query(F.data == 'ct')
async def set_lesson(call: types.CallbackQuery):
    global day
    now = datetime.datetime.today()
    day = 3
    if now.weekday() > day and not night:
        await call.message.answer(another_text, reply_markup=date)
    else:
        await call.message.answer(set_lesson_text, reply_markup=lesson)


@router.callback_query(F.data == 'pt')
async def set_lesson(call: types.CallbackQuery):
    global day
    now = datetime.datetime.today()
    day = 4
    if now.weekday() > day and not night:
        await call.message.answer(another_text, reply_markup=date)
    else:
        await call.message.answer(set_lesson_text, reply_markup=lesson)


@router.callback_query(F.data == 'sb')
async def set_lesson(call: types.CallbackQuery):
    global day
    now = datetime.datetime.today()
    day = 5
    if now.weekday() > day and not night:
        await call.message.answer(another_text, reply_markup=date)
    else:
        await call.message.answer(set_lesson_text, reply_markup=lesson)


@router.callback_query(F.data == 'vs')
async def set_lesson(call: types.CallbackQuery):
    global day
    now = datetime.datetime.today()
    day = 6
    if now.weekday() > day and not night:
        await call.message.answer(another_text, reply_markup=date)
    else:
        await call.message.answer(set_lesson_text, reply_markup=lesson)


# ----------------------------LESSONS------------------------------


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
async def text_hw(msg: Message, state: FSMContext):
    now = datetime.datetime.now().date()
    rev = False
    if night:
        now += datetime.timedelta(days=7)
    while now.weekday() != day:
        if rev:
            now -= datetime.timedelta(days=1)
        else:
            now += datetime.timedelta(days=1)
        if now.weekday() != day and now.weekday() == 6:
            rev = True
    db_sess = db_session.create_session()
    task = Tasks()
    klass_id = db_sess.query(User).filter(User.telegram_id == msg.from_user.username).first().current_class_id
    subj = db_sess.query(K_subject).filter(K_subject.name == nope[work]).first()
    rasps = db_sess.query(Rasp).filter(Rasp.klass_id == klass_id, Rasp.subject == subj).all()
    rasp = [el for el in rasps if el.start_time.date() == now]
    if not rasp:
        await msg.answer(f"Этого предмета нет в {yep[day]}", reply_markup=week)
    task.rasp = rasp[0]
    task.descriptions = msg.text
    task.creator = f"{msg.from_user.username}"
    task_type = db_sess.query(K_task_type).filter(K_task_type.id == hw_id).first()
    task_type.task.append(task)
    db_sess.commit()
    if admin:
        await msg.answer(added_text, reply_markup=ad)
    else:
        await msg.answer(added_text, reply_markup=men)
    await state.set_state(States.none)


@router.callback_query(F.data == 'photo')
async def set_hw(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(set_hw_photo, reply_markup=end)
    await state.set_state(States.photo)


@router.message(States.photo)
async def photo_hw(msg: types.Message, bot: Bot, state: FSMContext):
    if msg.photo:
        now = datetime.datetime.now().date()
        rev = False
        if night:
            now += datetime.timedelta(days=7)
        while now.weekday() != day:
            if rev:
                now -= datetime.timedelta(days=1)
            else:
                now += datetime.timedelta(days=1)
            if now.weekday() != day and now.weekday() == 6:
                rev = True
        db_sess = db_session.create_session()
        klass_id = db_sess.query(User).filter(User.telegram_id == msg.from_user.username).first().current_class_id
        subj = db_sess.query(K_subject).filter(K_subject.name == nope[work]).first()
        rasps = db_sess.query(Rasp).filter(Rasp.klass_id == klass_id, Rasp.subject == subj).all()
        rasp = [el for el in rasps if el.start_time.date() == now]
        if not rasp:
            await msg.answer(f"Этого предмета нет в {yep[day]}", reply_markup=week)
        file_name = f"photos/{msg.photo[-1].file_id}.jpg"
        await bot.download(msg.photo[-1], destination=file_name)
        task = Tasks()
        task.descriptions = f'{file_name}'
        task.creator = f"{msg.from_user.username}"
        task_type = db_sess.query(K_task_type).filter(K_task_type.id == hw_id).first()
        task_type.task.append(task)
        task.rasp = rasp[0]
        db_sess.commit()
        if admin:
            await msg.answer(added_text, reply_markup=ad)
        else:
            await msg.answer(added_text, reply_markup=men)
        await state.set_state(States.none)


@router.message(Command("start"))
async def start_handler(msg: Message, state: FSMContext):
    await msg.answer('Введите название вашего класса')
    await state.set_state(States.true)


@router.message(States.true)
async def checking(msg: Message, state: FSMContext):
    db_sess = db_session.create_session()
    klass = db_sess.query(K_klass).filter(K_klass.name == msg.text).first()
    if klass:
        access = db_sess.query(Access).filter(Access.telegram_id == msg.from_user.username,
                                          Access.klass == klass).first()
        if access:
            user = access.user
            user.current_class_id = klass.id
            db_sess.commit()
            await msg.answer('Вы успешно вошли в свой класс!')
            await state.set_state(States.none)
        else:
            await msg.answer('Вы не состоите в этом классе, введите ещё раз')
    else:
        await msg.answer('Такого класса не существует, введите ещё раз!')


@router.message(F.text.lower() == "меню")
@router.message(Command('menu'))
@router.message(States.none)
async def menu(msg: Message):

    if admin:
        await msg.answer(menu_text, reply_markup=ad)
    else:
        await msg.answer(menu_text, reply_markup=men)


@router.callback_query(F.data == 'menu')
async def menu(call: types.CallbackQuery):
    if admin:
        await call.message.answer(menu_text, reply_markup=ad)
    else:
        await call.message.answer(menu_text, reply_markup=men)


async def main():
    bot = Bot(token="7045128937:AAHTFOnWH-5TnaeHTwCqCFAGkoczGs0_57g", parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())