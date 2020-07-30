#!/usr/bin/env python
import os
import sys

from telegram.ext import Updater

if __name__ == "__main__":
    import os

    TOKEN = "1085962867:AAHQyGzmCyKJDfXGNmBgGVpt6Knb_eSzdE8"
    PORT = int(os.environ.get('PORT', '8443'))
    updater = Updater(TOKEN)
    # add handlers
    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=TOKEN)
    updater.bot.set_webhook("https://<appname>.herokuapp.com/" + TOKEN)
    updater.idle()
