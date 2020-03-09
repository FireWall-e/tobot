def Main(dbConfig, requestParams):
    return renderTodoPage(dbConfig, requestParams['id']) if 'id' in requestParams else renderTodosPage(dbConfig)

def renderTodoPage(dbConfig, todoId):
    from functions.main import getMilliseconds

    todo = getTodo(dbConfig, todoId)
    todoHTML = \
        """
            <div class="todo page">
                <input class="todo__item title" value="{title}"></input>
                <textarea class="todo__item text">{text}</textarea>
                <div class="todo__item">
                    <div class="todo__column remind" title="Remind time should be greater then 10 minutes and less then a year">
                        <span class="label">Remind at:</span>
                        <div class="datepicker">
                            <input type="text" name="date" class="datepicker__item date" pattern="^(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[012])\.(19|20)\d\d$" placeholder="Date (dd.mm.yy)" title="Format (dd.mm.yyyy), example - 01.11.2011" value="" required/>
                            <input type="text" name="time" class="datepicker__item time" pattern="^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$" placeholder="Time 24-h (hh:mm)" title="24-hour format (hh:mm), example - 08:30" value="" required/>
                        </div>
                    </div>
                </div>
            </div>
        """\
        .format(
            title = todo['title'],
            text = todo['text'],
            remindAt = todo['remind_at'],
        ) 
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
        serverTimeMS = getMilliseconds()
    )

def getTodo(dbConfig, todoId):
    import dataset
    db = dataset.connect(dbConfig['url'])
    table = db['todos']
    todo = table.find_one(todo_id = todoId)
    return todo

def renderTodosPage(dbConfig):
    todos = getTodos(dbConfig)
    todosHTML = renderItems(todos)
    containerClass = ' empty' if not todosHTML else ''
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
            <script type="text/javascript" src="/assets/js/todo/main.js"></script>
        </head>
        <body>
            <main class="main image image--todo">
                <section class="content">
                    <div class="panel">
                        <button class="panel__item hover--zoom" title="Add todo" onclick="App.todo.add();"><i class="icon icon--add-todo"></i></button>
                        <button class="panel__item hover--zoom" title="Delete all todos" onclick="App.todo.deleteAll();"><i class="icon icon--delete-todos"></i></button>
                    </div>
                    <div class="container{containerClass}">
                        <div class="todos page">{todosHTML}</div>
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
        containerClass = containerClass,
        todosHTML = todosHTML
    )

def getTodos(dbConfig):
    import dataset
    db = dataset.connect(dbConfig['url'])
    table = db['todos']
    # print('todos are ', )
    return table.all()

def renderItems(todos):
    html = ''
    for todo in todos:
        print('todo is ', todo)
        html += \
        """
            <div class="todo">
                <span class="todo__item title">{title}</span>
                <span class="todo__item text">{text}</span>
                <div class="todo__item">
                    <div class="todo__column remind">
                        <span class="label">Remind at:</span>
                        <span class="date">{remindAt}</span>
                    </div>
                    <div class="todo__column buttons">
                        <button class="todo__edit todo-button hover--zoom" title="Edit todo" onclick="App.todo.edit({todoId});"><i class="icon icon--edit-todo"></i></button>
                        <button class="todo__delete todo-button hover--zoom" title="Delete todo" onclick="App.todo.delete({todoId});"><i class="icon icon--delete-todo"></i></button>
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
    