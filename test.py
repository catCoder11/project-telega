from telegram.ext import CommandHandler, Application
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from datetime import datetime as dt

BOT_TOKEN = "7087953766:AAHZhEaNOHUwuVr-49sizlgdCG-i7LgZz3w"

adm = False

st = [['/start']]
basic = [['/admin_on'], ['/add_homework', '/get_homework'], ['/close']]
ad_com = [['add_homework', 'get_homework'], ['/admin_off']]
markup = ReplyKeyboardMarkup(basic, one_time_keyboard=False)
admin_commands = ReplyKeyboardMarkup(ad_com, one_time_keyboard=False)
starts = ReplyKeyboardMarkup(st, one_time_keyboard=False)


async def admin_on(update, context):
    await update.message.reply_text('вы вошли в режим админа',
                                    reply_markup=admin_commands)


async def admin_off(update, context):
    await update.message.reply_text('вы больше не админ',
                                    reply_markup=markup)


async def add_individual_hw(update, context):
    await update.message.reply_text(
        "тут пока ничего нет")


async def start(update, context):
    await update.message.reply_text(
        "работа начата",
        reply_markup=markup
    )


async def get(update, context):
    await update.message.reply_text('тут пока ничего нет')


async def close(update, context):
    await update.message.reply_text(
        "работа окончена",
        reply_markup=starts
    )


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("admin_off", admin_off))
    application.add_handler(CommandHandler("admin_on", admin_on))
    application.add_handler(CommandHandler("get_homework", get))
    application.add_handler(CommandHandler('close', close))
    application.add_handler(CommandHandler("add_homework", add_individual_hw))
    application.add_handler(CommandHandler("start", start))
    application.run_polling()


if __name__ == '__main__':
    main()
