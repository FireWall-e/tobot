def Main(actionName, payload, dbConfig):
    # print('KOK', doAction)
    import dataset

    db = dataset.connect(dbConfig['url'])
    # print('OK')
    # return doAction(actionName, {'payload': payload, 'db': db})
    return globals()[actionName](payload, db)

def verifyUserToken(payload, _):
    from api.jwt.main import decode
    encryptedPayload = decode(payload['token'])
    # print('token is ', ecryptedPayload)
    return 'true' if encryptedPayload else ''

def create(payload, db):
    from api.jwt.main import decode
    username = decode(payload['token'])['username']

    table = db['todos']
    rowId = table.insert({
        'username': username,
        'todo_id': payload['todoId'],
        'title': '',
        'text': '',
        'remind_at': ''
    })
    todos = table.all()
    for todo in todos:
        print('db todos table row is ', todo)
    # print('rowid is ', rowId)
    return rowId if rowId else ''

def save(payload, db):
    tableTodos = db['todos']
    updateData = {
        'todo_id': payload['todoId'],
        'title': payload['title'],
        'text': payload['text'],
    }

    
    # print('path is ', ROOT)
    print('payload is ', payload)
    # print('os is2 ', os.getcwd())
    # users = tableUsers.all()
    # for user in users:
    #     print('db users table row is ', user)
    
    
    # print('PATH IS ', getPythonExePath())
    from functions.main import executeCommand
    todo = tableTodos.find_one(todo_id = payload['todoId'])
    if not 'remindAtMDYArray' in payload and todo['remind_at']: # Если хотим убрать напоминалку
        updateData['remind_at'] = ''
        executeCommand('schtasks /delete /tn "Remind{todoId}" /f'.format(todoId = payload['todoId']))

    # print('__file__ is ', __file__)
    # executeCommand('timeout /t 2 /nobreak & C:\Data\Pynaconda\python C:/Data/Web/projects/tobot/api/telegram/notifyUser.py')
    if 'remindAtMDYArray' in payload: # Если хотим добавить напоминалку
        # from api.telegram.notifyUser import __file__
        from functions.main import getPythonExePath
        from api.jwt.main import decode
        import os

        if todo['remind_at']:
            executeCommand('schtasks /delete /tn "Remind{todoId}" /f'.format(todoId = payload['todoId']))

        tableUsers = db['users']
        username = decode(payload['token'])['username']
        print('username is ', username)
        user = tableUsers.find_one(username = username)
        print('user found ', user)



        commandToExecute = \
        'schtasks /create /tn "Remind{todoId}" /tr "{toRun} {arguments}" /sc once /sd {dateMDY} /st {time}' \
        .format(
            todoId = payload['todoId'],
            toRun = '{pythonExePath} {fileToRunPath}'.format(
                pythonExePath = getPythonExePath().replace('\\', '/'),
                fileToRunPath = '{appRootDir}/api/telegram/notifyUser.py'.format(appRootDir = os.getcwd().replace('\\', '/'))
            ),
            arguments = '{chatId} {message} {parseMode}'.format(
                chatId = '--chat_id {chatId}'.format(chatId = user['chat_id']),
                message = '--message \\"Hi, @{username}! Please dont forget about {link}'.format(
                    username = username,
                    link = '[{title}](http://127.0.0.1:80/todo?id={todoId}) todo. Have a nice day ! :)\\"'.format(
                        title = payload['title'],
                        todoId = payload['todoId']
                    )
                ),
                parseMode = '--parse_mode Markdown'
            ),
            dateMDY = payload['remindAtMDYArray'][0],
            time = payload['remindAtMDYArray'][1]
        )
        # import generate command
        print('command to execute is ', commandToExecute)
        executeCommand(commandToExecute)

        updateData['remind_at'] = payload['remindAt']
        # print('MEEEEEEEEEE', payload['remindAtMDYArray'])
        # command = createTimeoutCommand(payload['timeoutS'], 'python C:/Data/Web/projects/tobot/api/telegram/notifyUser.py')
        # print('command is ', command)
        # execute command
    return tableTodos.update(updateData, ['todo_id'])