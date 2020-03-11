def Main(actionName, payload, dbConfig):
    # print('KOK', doAction)
    import dataset

    db = dataset.connect(dbConfig['url'])
    # print('OK')
    # return doAction(actionName, {'payload': payload, 'db': db})
    return globals()[actionName](payload, db)

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

def delete(payload, db):
    from api.jwt.main import decode

    username = decode(payload['token'])['username']
    if username:
        from functions.main import executeCommand

        executeCommand('schtasks /delete /tn "Remind{todoId}" /f > nul 2> nul'.format(todoId = payload['todoId']))
        table = db['todos']
        
        return table.delete(username = username, todo_id = payload['todoId'])
    return ''

def deleteAll(payload, db):
    from api.jwt.main import decode
    print('payload is ', payload)
    username = decode(payload['token'])['username']
 
    if username:
        from functions.main import executeCommand

        table = db['todos']
        todos = table.find(username = username)

        for todo in todos:
            executeCommand('schtasks /delete /tn "Remind{todoId}" /f > nul 2> nul'.format(todoId = todo['todo_id']))

        return table.delete(username = username)
    return ''

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
                    link = '[{title}](http://127.0.0.1:80/todo?id={todoId})! :)\\"'.format(
                        title = payload['title'] or 'none',
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

def verifyUserToken(payload, db):
    from api.jwt.main import decode
    username = decode(payload['token'])['username']
    # print('token is ', ecryptedPayload)
    # print(encryptedPayload is )
    if not username:
        return 'invalidToken'
    # print('todos are ', getTodos(username, db))
    todos = getTodos(username, db)
    return renderItems(todos)

def getTodos(username, db):
    return db.query(
        'SELECT * FROM todos WHERE username = :username ORDER BY id DESC', 
        { 'username': username }
    )

def renderItems(todos):
    html = ''
    for todo in todos:
        print('todo is ', todo)
        html += \
        """
            <div class="todo" data-id="{todoId}">
                <span class="todo__item title">{title}</span>
                <span class="todo__item text">{text}</span>
                <div class="todo__item">
                    <div class="todo__column remind" title="Time when you will be notified">
                        <span class="label">Remind at:</span>
                        <span class="date">{remindAt}</span>
                    </div>
                    <div class="todo__column buttons">
                        <button class="todo__edit todo-button hover--zoom" title="Edit todo" onclick="App.todo.edit({todoId});"><i class="icon icon--edit-todo"></i></button>
                        <button class="todo__delete todo-button hover--zoom" title="Delete todo" onclick="App.todo.delete({todoId}, true);"><i class="icon icon--delete-todo"></i></button>
                    </div>
                </div>
            </div>
        """\
        .format(
            todoId = todo['todo_id'],
            title = todo['title'],
            text = todo['text'],
            remindAt = todo['remind_at']
        )
    return html
