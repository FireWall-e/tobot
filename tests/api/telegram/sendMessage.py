# from api.telegram.main import url
from api.telegram.notifyUser import sendTelegramMessage

print('[tests]: api/telegram/sendMessage | output is ', sendTelegramMessage(596421831, 'Test message'))

