#!/usr/bin/env python
import os
import sys

import telebot

TOKEN = "1085962867:AAHQyGzmCyKJDfXGNmBgGVpt6Knb_eSzdE8"

bot = telebot.TeleBot(TOKEN)


def start_callback(update, context):
    update.message.reply_text("Welcome to my awesome bot!")


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)


bot.polling()
