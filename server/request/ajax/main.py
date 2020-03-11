import json

def Main(postData, handlerFilename, dbConfig, dynamicImportModule):
    # print('AJAX HANDLER', postData, 'FILENAME IS ', handlerFilename)
    ajaxHandlersModulePath = 'server.request.ajax.handlers.'
    postData = json.loads(postData.getvalue('data'))
    # print('FAIL ',postData)
    # x = {
    #     "name": "John",
    #     "age": 30,
    #     "city": "New York"
    # }
    # print(dynamicImportModule(ajaxHandlersModulePath + handlerFilename, 'Main')())
    # '''Должно быть примерно так'''
    # print('FOK', doAction)
    kwargs = {
        'actionName': postData['doAction'],
        'payload': postData['payload'] if 'payload' in postData else False,
        'dbConfig': dbConfig,
        # 'doAction': doAction
    }

    resultData = dynamicImportModule(ajaxHandlersModulePath + handlerFilename, 'Main')(**kwargs)
    # print('resultData is ', resultData)
    return json.dumps(resultData or '')

# Ошибка скоупа
# def doAction(actionName, kwargs):
#     getattr(sys.modules[__name__], actionName)(**kwargs)