from telegram.ext import CommandHandler, Application, filters, MessageHandler
from telegram import ReplyKeyboardMarkup
import sqlite3

BOT_TOKEN = "7087953766:AAHZhEaNOHUwuVr-49sizlgdCG-i7LgZz3w"

hw = False

st = [['/start']]
basic = [['/admin_on'], ['/add_your_homework', '/get_homework'], ['/close']]
ad_com = [['/set_homework'], ['/admin_off']]
markup = ReplyKeyboardMarkup(basic, one_time_keyboard=False)
admin_commands = ReplyKeyboardMarkup(ad_com, one_time_keyboard=False)
starts = ReplyKeyboardMarkup(st, one_time_keyboard=False)


async def echo(update, context):
    global hw
    sql = sqlite3.connect('something_test.sqlite')
    cur = sql.cursor()
    result = cur.execute("""INSERT INTO something(individual_hw) VALUES(?)""",
                         (update.message.text, ))
    hw = False


async def homework(update, context):
    await update.message.reply_text(
        "тут пока ничего нет")


async def admin_on(update, context):
    await update.message.reply_text('вы вошли в режим админа',
                                    reply_markup=admin_commands)


async def admin_off(update, context):
    await update.message.reply_text('вы больше не админ',
                                    reply_markup=markup)


async def add_individual_hw(update, context):
    global hw
    hw = True
    await update.message.reply_text(
        "впишите вашу домашку")


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
    global hw
    application = Application.builder().token(BOT_TOKEN).build()
    if hw:
        application.add_handler(MessageHandler(filters.TEXT, echo))

    else:
        application.add_handler(CommandHandler("admin_off", admin_off))
        application.add_handler(CommandHandler("admin_on", admin_on))

        application.add_handler(CommandHandler("get_homework", get))
        application.add_handler(CommandHandler('close', close))
        application.add_handler(CommandHandler("add_your_homework",
                                               add_individual_hw))
        application.add_handler((CommandHandler('set_homework', homework)))
        application.add_handler(CommandHandler("start", start))
    application.run_polling()


if __name__ == '__main__':
    main()
