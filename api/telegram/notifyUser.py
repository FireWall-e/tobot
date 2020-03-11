# CLI run command:> python notifyUser.py --chat_id [id] --message [message]

import requests
from argparse import ArgumentParser
import sys
# from api.telegram.main import url
botToken = '1135448518:AAGS2SxWLmiqyDIm3cVQft4BGKHINxSw4So'
url = 'https://api.telegram.org/bot' + botToken + '/sendMessage'

def parseCL():
    parser = ArgumentParser()
    parser.add_argument("-ci", "--chat_id",
                        help="Telegram's bot chat id")
    parser.add_argument("-m", "--message",
                        help="Message to be sent https://core.telegram.org/bots/api#sendmessage")
    parser.add_argument("-pm", "--parse_mode",
                    help="Parse mode parameter https://core.telegram.org/bots/api#markdown-style")
    return parser.parse_args()

def sendTelegramMessage(chatId, message, parseMode):
    params = {
        'chat_id': chatId,
        'text': message,
        'parse_mode': parseMode
    }

    response = requests.get(url, params)
    print('response is         ', response)


def Main():
    args = parseCL()

    # import db check if todo still relevant
    # print('received ', args)
    sendTelegramMessage(args.chat_id, args.message, args.parse_mode)
    # sendTelegramMessage(596421831, 'testme')

Main()