def Main(dbConfig, requestParams):
    # Если в адресной строке присуствует параметр запроса id (?id=) то рендерим страницу 1 todo,
    # в противном случае рендерим страницу со всеми todo
    return renderTodoPage(dbConfig, requestParams['id'][0]) if 'id' in requestParams else renderTodosPage()

# Рендерим страницу единичной todo (запрос по ?id=) 
def renderTodoPage(dbConfig, todoId):
    from functions.main import getDateMilliseconds

    # Вытаскиваем данные todo по id из БД
    todo = getTodo(dbConfig, todoId)

    # Дефолтные параметры
    date = ''
    time = ''

    # Если у записи есть дата напоминания - строка вида '[дата] [время]', то разбиваем 
    # на соответствующие отдельные переменные
    if todo['remind_at']:
        dateTime = todo['remind_at'].split(' ')
        date = dateTime[0]
        time = dateTime[1]

    # html строка нашего todo
    todoHTML = \
        """
            <div class="todo page">
                <input class="todo__item title" value="{title}"></input>
                <textarea class="todo__item text">{text}</textarea>
                <div class="todo__item">
                    <div class="todo__column remind" title="Remind time should be greater then 5 minutes and less then a year">
                        <span class="label">Remind at:</span>
                        <div class="datepicker">
                            <input type="text" name="date" class="datepicker__item date" pattern="^(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[012])\.(19|20)\d\d$" placeholder="Date (dd.mm.yy)" title="Format (dd.mm.yyyy), example - 01.11.2011" value="{date}" required/>
                            <input type="text" name="time" class="datepicker__item time" pattern="^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$" placeholder="Time 24-h (hh:mm)" title="24-hour format (hh:mm), example - 08:30" value="{time}" required/>
                        </div>
                    </div>
                </div>
            </div>
        """\
        .format( # Подставляем данные в строку по соответствующим ключам (placeholders) {}
            title = todo['title'],
            text = todo['text'],
            date = date,
            time = time
        ) 

    # Возвращаем html полноценной страницы с подстановной переменных в {}, как ранее
    return """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Tobot - todo</title>

            <link rel="stylesheet" href="/assets/css/main.css">
            <link rel="stylesheet" href="/assets/css/todo/main.css">

            <script>
                'use strict';
                const serverTimeMS = {serverTimeMS};
            </script>
            <script type="text/javascript" src="/assets/js/todo/main.js"></script>
        </head>
        <body>
            <main class="main image image--todo">
                <section class="content">
                    <div class="panel">
                        <button class="panel__item hover--zoom" title="Back to list" onclick="App.return();"><i class="icon icon--return"></i></button>
                        <button class="panel__item hover--zoom" title="Save changes" onclick="App.todo.save({todoId});"><i class="icon icon--save-todo"></i></button>
                        <button class="panel__item hover--zoom" title="Discard changes" onclick="App.todo.discard({todoId});"><i class="icon icon--discard-todo"></i></button>
                        <button class="panel__item hover--zoom" title="Delete todo" onclick="App.todo.delete({todoId});"><i class="icon icon--delete-todo"></i></button>
                    </div>
                    <div class="container">
                        <div class="todos">{todoHTML}</div>
                    </div>
                </section>
                <div class="modal show loading">
                    <i class="spinner icon icon--loading"></i>
                </div>
            </main>
        </body>
        </html>
    """\
    .format(
        todoId = todoId,
        todoHTML = todoHTML,
        serverTimeMS = getDateMilliseconds()
    )

# Вытаскиваем данные todo по ее id из БД
def getTodo(dbConfig, todoId):
    import dataset
    db = dataset.connect(dbConfig['url'])
    table = db['todos']
    todo = table.find_one(todo_id = todoId)
    return todo

# Рендерим страницу со всеми todo
def renderTodosPage():
    from functions.main import getDateMilliseconds

    return \
    """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Tobot - todo</title>
            <link rel="stylesheet" href="/assets/css/main.css">
            <link rel="stylesheet" href="/assets/css/todo/main.css">
            <script>
                'use strict';
                const serverTimeMS = {serverTimeMS};
            </script>
            <script type="text/javascript" src="/assets/js/todo/main.js"></script>
        </head>
        <body>
            <main class="main image image--todo">
                <section class="content">
                    <div class="panel">
                        <button class="panel__item hover--zoom" title="Log-out" onclick="App.logout();"><i class="icon icon--logout"></i></button>
                        <button class="panel__item hover--zoom" title="Add todo" onclick="App.todo.add();"><i class="icon icon--add-todo"></i></button>
                        <button class="panel__item hover--zoom" title="Delete all todos" onclick="App.todo.deleteAll();"><i class="icon icon--delete-todos"></i></button>
                    </div>
                    <div class="container empty">
                        <div class="todos page"></div>
                    </div>
                </section>
                <div class="modal show loading">
                    <i class="spinner icon icon--loading"></i>
                </div>
            </main>
        </body>
        </html>
    """\
    .format( # Записываем переменную непосредственно в константу JavaScriptб для дальнейшего учета времени на стороне клиента (в браузере)
        serverTimeMS = getDateMilliseconds()
    )
    