import os

import requests
from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

load_dotenv()

token = os.getenv('TOKEN')

updater = Updater(token=token)


CAT_URL = 'https://api.thecatapi.com/v1/images/search'
DOG_URL = 'https://api.thedogapi.com/v1/images/search'


def get_new_cat_image():
    try:
        response = requests.get(CAT_URL).json()
    except Exception as error:
        print(error)
        response = requests.get(DOG_URL)

    random_cat = response[0].get('url')
    return random_cat


def new_cat(update, context):
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_new_cat_image())


def get_new_dog_image():
    response = requests.get(DOG_URL).json()
    random_dog = response[0].get('url')
    return random_dog


def new_dog(update, context):
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_new_dog_image())


def wake_up(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    button = ReplyKeyboardMarkup([['/newcat'], ['/newdog']], resize_keyboard=True)

    context.bot.send_message(
        chat_id=chat.id,
        text=f'{name}, look who i found for you!',
        reply_markup=button
    )
    context.bot.send_photo(chat.id, get_new_cat_image())


updater.dispatcher.add_handler(CommandHandler('start', wake_up))
updater.dispatcher.add_handler(CommandHandler('newcat', new_cat))
updater.dispatcher.add_handler(CommandHandler('newdog', new_dog))

updater.start_polling()
updater.idle()
