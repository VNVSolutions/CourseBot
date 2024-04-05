from time import sleep

import telebot
from django.conf import settings

TOKEN = '7188089434:AAFBMQz7bQbjG7Q7dkETWU6PCeERkkf4i5Q'

# Ініціалізуємо телеграм-бота
bot = telebot.TeleBot(TOKEN)


# Встановлюємо вебхук
bot.remove_webhook()
bot.set_webhook(url=settings.WEBHOOK_URL)