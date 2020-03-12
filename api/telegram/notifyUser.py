# Библиотека для работы с http запросами
import requests
# Библиотека для парса аргументов командной строки
from argparse import ArgumentParser
import sys

# Токен нашего бота, который генерируется у BotFather при создании бота - команда /newbot
# /setuserpic Команда для присвоения аватарки боту
# https://telegram.me/BotFather
# https://core.telegram.org/bots/api
botToken = '1135448518:AAGS2SxWLmiqyDIm3cVQft4BGKHINxSw4So'
# Ссылка для отправки сообщения бота пользователю
# https://core.telegram.org/bots/api#sendmessage
url = 'https://api.telegram.org/bot' + botToken + '/sendMessage'

# Функция парса аргументов
# может принять такие аргументы, как
# chat_id, message и parse_mode
def parseCL():
    parser = ArgumentParser()
    parser.add_argument("-ci", "--chat_id",
                        help="Telegram's bot chat id")
    parser.add_argument("-m", "--message",
                        help="Message to be sent https://core.telegram.org/bots/api#sendmessage")
    parser.add_argument("-pm", "--parse_mode",
                    help="Parse mode parameter https://core.telegram.org/bots/api#markdown-style")
    return parser.parse_args()

# Функция, которая отправляет сообщение пользователю с указанными параметрами
def sendTelegramMessage(chatId, message, parseMode):
    params = {
        'chat_id': chatId,
        'text': message,
        'parse_mode': parseMode
    }

    requests.get(url, params)


def Main():
    # Парсим аргументы командной строки
    args = parseCL()
    # Отправляем сообщение с полученными аргументами
    sendTelegramMessage(args.chat_id, args.message, args.parse_mode)

# Вызываем мгновенно
Main()