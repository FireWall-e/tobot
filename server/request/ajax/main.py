# Библиотека для работы с данными в формате json
import json

# Функция которая будет вызвана в requestHandler автоматически
def Main(postData, handlerFilename, dbConfig, dynamicImportModule):
    # Модульный путь к файлам обработчикам
    ajaxHandlersModulePath = 'server.request.ajax.handlers.'
    # Преобразовываем (парсим) полученные данные
    # https://www.w3schools.com/python/python_json.asp
    postData = json.loads(postData.getvalue('data'))
 
    kwargs = {
        'actionName': postData['doAction'], # Обязательный аргумент, содержит имя действие (функции), которую нужно выполнить
        'payload': postData['payload'] if 'payload' in postData else False, # Дополнительнные (опциональные) данные которые нужно обработать
        'dbConfig': dbConfig,
    }
    # Динамически подключаем непосредственно сам файлик обработчик, вызывае его Main функцию, с переменными kwargs
    resultData = dynamicImportModule(ajaxHandlersModulePath + handlerFilename, 'Main')(**kwargs)
    # Отдаем клиенту (опциональные) данные в формате json (пустую строку если ничего не вернулось)
    return json.dumps(resultData or '')