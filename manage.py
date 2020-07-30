#!/usr/bin/env python
import os
import sys

from telegram import Bot
from telegram.ext import Updater, Dispatcher


def start_callback(update, context):
    update.message.reply_text("Welcome to my awesome bot!")


def main():
    import os

    TOKEN = "1085962867:AAHQyGzmCyKJDfXGNmBgGVpt6Knb_eSzdE8"
    PORT = int(os.environ.get('PORT', '8443'))
    updater = Updater(TOKEN)
    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=TOKEN)
    updater.bot.set_webhook("https:///mysterious-sierra-44668.herokuapp.com/" + TOKEN)

    updater.dispatcher.add_handler(start_callback)

    updater.idle()


print("started 1", file=open('file.txt', 'w'))
main()
print("ended 1", file=open('file.txt', 'w'))

