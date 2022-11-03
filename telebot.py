import os
from dotenv import load_dotenv
import telegram
from telegram.ext import Updater, Filters, MessageHandler

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')


bot = telegram.Bot(token=TELEGRAM_TOKEN)
updater = Updater(token=TELEGRAM_TOKEN)
dp = updater.dispatcher


def send_message(message):
    bot.send_message(chat_id=CHAT_ID, text=message)


def text_message_controler(update, context):
    chat = update.effective_chat
    text_mesage = update.message.text
    context.bot.send_message(chat_id=chat.id, text=text_mesage)


# тут обрабатываются текстовые сообщения (str) и разные типы файлов.
dp.add_handler(MessageHandler(Filters.text, text_message_controler))

updater.start_polling(poll_interval=5.0)
################
# Бот будет работать до тех пор, пока не нажмете Ctrl-C
updater.idle()
################
