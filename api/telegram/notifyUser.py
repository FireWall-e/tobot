# CLI run command:> python notifyUser.py --chat_id [id] --message [message]

import requests
from argparse import ArgumentParser
import sys

botToken = '1135448518:AAGS2SxWLmiqyDIm3cVQft4BGKHINxSw4So'
url = 'https://api.telegram.org/bot' + botToken + '/sendMessage'

def parseCL():
    parser = ArgumentParser()
    parser.add_argument("-ci", "--chat_id",
                        help="Telegram's bot chat id")
    parser.add_argument("-m", "--message",
                        help="Message to be sent")
    return parser.parse_args()

def sendTelegramMessage(chatId, message):
    params = {
        'chat_id': chatId,
        'text': message
    }

    requests.get(url, params) 


def Main():
    args = parseCL()
    sendTelegramMessage(args.chatId, args.message)

Main()