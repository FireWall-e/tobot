# Функция которая будет вызвана мгновенно
# Принимает название действия (функции) - actionName
# Данные со стороны клиента - payload
# И ссылку на БД - dbConfig
def Main(actionName, payload, dbConfig):
    # Библиотека для работы с БД
    # https://dataset.readthedocs.io/en/latest/
    import dataset
    # Подключаемся к БД
    # https://dataset.readthedocs.io/en/latest/api.html#connecting
    db = dataset.connect(dbConfig['url'])
    # Возвращаем результат выполнения функции с динамическим именем actionNaem
    # Например, если actionName = 'create', то выполнится функция create, которая описана ниже
    # С передачей таких параметров как (опциональные) данные со стороны клиента - payload
    # И базой данных
    return globals()[actionName](payload, db)
# Функция, которая отвечает за запись (инициализацию) нового todo в соответствующую таблицу БД - todos
def create(payload, db):
    # Имортируем нашу обертку (wrapper) для работы с токенами
    # А именно функцию decode, которая принимает токен и отдает зашифрованные в нем данные (username)
    # https://jwt.io/introduction/
    from api.jwt.main import decode
    # Получаем имя пользователя из токена
    # Если токен более не валидный (просроченый - в текущий момент действителен не более 1 дня с момента логина), 
    # то вернет False
    username = decode(payload['token'])['username']
    # Подключаемся к таблице
    table = db['todos']
    # Вставляем новую запись (строку) в таблицу
    # И получаем id вставленной строки - rowId
    # Записываем также username, для того чтобы каждый пользователь имел свой список todo, 
    # а не один на всех пользователей
    # Будет использоваться в дальнейнем для того чтобы получить все todo записи пользователя по его username
    # https://dataset.readthedocs.io/en/latest/api.html#dataset.Table.insert
    rowId = table.insert({
        'username': username,
        'todo_id': payload['todoId'],
        'title': '',
        'text': '',
        'remind_at': ''
    })
    # Если запись прошла успешно, то возвращаем ее id, в противном случае - ничего
    return rowId if rowId else ''
# Функция удаления записи (строки) из таблицы
def delete(payload, db):
    from api.jwt.main import decode
    # Принцип тот же - достаем username из токена, чтобы удалить запись конкретного пользователя
    username = decode(payload['token'])['username']
    # Если токен еще валидный
    if username:
        # Импортируем из функций executeCommand, которая позволяет вызвать cmd команду из python
        from functions.main import executeCommand
        # Команда удаляет задание из планировщика задания с названием Remind{айдиTodoКоторуюНужноУдалить}
        # > nul 2> nul - Игнорирует ошибки, например, если задание уже было удалено ранее
        # https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/schtasks#BKMK_delete
        executeCommand('schtasks /delete /tn "Remind{todoId}" /f > nul 2> nul'.format(todoId = payload['todoId']))
        table = db['todos']
        # Удаляем запись из таблицы
        return table.delete(username = username, todo_id = payload['todoId'])
    return ''
# Предназначена для удаления всех todo записей пользователя
def deleteAll(payload, db):
    from api.jwt.main import decode
   
    username = decode(payload['token'])['username']
     # Аналогично проверяем валидность токена
    if username:
        from functions.main import executeCommand

        table = db['todos']
        # Находим все записи принадлежащие пользователю с определенным username
        todos = table.find(username = username)
        # Для каждой вызываем команду удаления задание из планировщика,
        # в случае если было запланировано напоминание
        for todo in todos:
            executeCommand('schtasks /delete /tn "Remind{todoId}" /f > nul 2> nul'.format(todoId = todo['todo_id']))
        # Удаляем все записи по полю username
        return table.delete(username = username)
    return ''
# Сохраняем изменения в редактируемой todo
def save(payload, db):
    tableTodos = db['todos']
    # Заготовка с новыми данными
    updateData = {
        'todo_id': payload['todoId'],
        'title': payload['title'],
        'text': payload['text'],
    }
    from functions.main import executeCommand
    # Достаем данные todo по ее id
    todo = tableTodos.find_one(todo_id = payload['todoId'])
    # Если мы не получили данные с датой и временем для напоминание, а напоминание уже запланировано
    if not 'remindAtMDYArray' in payload and todo['remind_at']: 
        # Обнуляем напоминание для записи
        updateData['remind_at'] = ''
        # Удаляем задание из планировщика
        executeCommand('schtasks /delete /tn "Remind{todoId}" /f > nul 2> nul'.format(todoId = payload['todoId']))
    # Если получили дату и время для напоминания
    if 'remindAtMDYArray' in payload:
        from functions.main import getPythonExePath
        from api.jwt.main import decode
        # Системная библиотека
        import os
        # Если хотим перезаписать дату и время уже запланированного задания
        # предварительно его нужно удалить, чтобы позже создать новое с новой датой и временем
        if todo['remind_at']:
            executeCommand('schtasks /delete /tn "Remind{todoId}" /f > nul 2> nul'.format(todoId = payload['todoId']))
        # Достаем данные пользователя по его username
        # Необходимо достать id чата, куда бот будет отправлять напоминание
        tableUsers = db['users']
        username = decode(payload['token'])['username']
        user = tableUsers.find_one(username = username)
        # Путь к текущей директории
        currentDir = os.path.dirname(__file__)
        # Достать текущий адрес ngrok из файла
        ngrokUrl = open(os.path.join(currentDir, 'ngrok.txt')).readline().strip()
        # Команда для создания нового "единоразового" задания в планировщике
        # После создания задание его можно просмотреть в планировщике заданий windows 
        # С соответствующим названием вида Remind{todoId}
        # Стоит учесть, что после выполнения задания, оно всеравно остается в планировщике
        # Его можно удалить вручную, или просто удалить запись. Также можно оставить поля даты и времени соответствующей записи
        # Пустыми с дальнейшем сохранением изменений
        # https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/schtasks#BKMK_once
        commandToExecute = \
        'schtasks /create /tn "Remind{todoId}" /tr "{toRun} {arguments}" /sc once /sd {dateMDY} /st {time}' \
        .format(
            todoId = payload['todoId'],
            toRun = '{pythonExePath} {fileToRunPath}'.format(
                pythonExePath = getPythonExePath().replace('\\', '/'), # Меняем backslash на обычный / , чтобы строка была интерпретирована правильно
                fileToRunPath = '{appRootDir}/api/telegram/notifyUser.py'.format(appRootDir = os.getcwd().replace('\\', '/')) # os.getcwd() возвращает путь к корню проекта
            ),
            arguments = '{chatId} {message} {parseMode}'.format( # Необходимо передать id чата, username и текст сообщения, а также parse mode для корректной интерпретации сообщения самим телеграмом
                chatId = '--chat_id {chatId}'.format(chatId = user['chat_id']), # фразы начинающиеся с '--' или '-' - это аргументы командной строки, которые принимает файл notifyUser.py
                message = '--message \\"Hi, @{username}! Please dont forget about {link}'.format(
                    username = username,
                    link = '[{title}]({ngrokUrl}/todo?id={todoId})! :)\\"'.format(
                        ngrokUrl = ngrokUrl or 'http://127.0.0.1:80',
                        title = payload['title'] or 'nothing', # Если у записи нет названия записи, то nothing по умолчанию
                        todoId = payload['todoId']
                    )
                ),
                parseMode = '--parse_mode Markdown'
            ),
            dateMDY = payload['remindAtMDYArray'][0], # Дата в формате Месяц/День/Год для напоминания
            time = payload['remindAtMDYArray'][1] # Время в 24-ом формате вида 00:00 для напоминания
        )
        # Выполняем команду
        executeCommand(commandToExecute)
        # Добавляем записи время когда нужно напомнить
        # Используется в основном в шаблоне, для наглядности
        updateData['remind_at'] = payload['remindAt']
    # Обновляем запись в таблице по полю todo_id и возвращаем результат
    # https://dataset.readthedocs.io/en/latest/api.html#dataset.Table.update
    return tableTodos.update(updateData, ['todo_id'])
# Функция для валидация токена
# Необходимо для просмотра записей на страницах записей (/todo) и отдельных записей (/todo?id=123456789)
def verifyUserToken(payload, db):
    from api.jwt.main import decode
    username = decode(payload['token'])['username']
    # Если токен просрочен, т.е. получили False в username
    if not username:
        return 'invalidToken'
    # Если токен валидный то достаем все todo текущего пользователя
    todos = getTodos(username, db)
    # Возвращаем результат рендера всех todo
    return renderItems(todos)
# Получаем все todo
def getTodos(username, db):
    return db.query( # Достаем все записи по username в порядке убывания, т.е. от самых свежих до более ранних
        'SELECT * FROM todos WHERE username = :username ORDER BY id DESC', 
        { 'username': username }
    )
# Функция рендера, которая принимает итерируемый объект с нашими todo
def renderItems(todos):
    # Заготовка
    html = ''
    # Генерируем html для каждого todo и записываем в результирующую переменную строку - html
    for todo in todos:
        # \ Используется для экранирования перехода на новую строку, дабы избежать синтаксической ошибки
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
        .format( # "Впечатываем" соответствубщие данные в конечный шаблон
            todoId = todo['todo_id'],
            title = todo['title'],
            text = todo['text'],
            remindAt = todo['remind_at']
        )
    # Возвращаем html со всеми todo
    return html
