// Нижеприведенный код выполнится после загрузки окна браузера - window.onload
window.onload = () => {
    // Некоторые объяснения были опущены, т.к. уже приведены для index страницы
    // Аналогичным образом инициализируем переменную App
    this.App = new function() {
        // Записываем серверное время в локальную переменную преобразовывая миллисекунды в секунды
        let localTimeS = parseInt((new Date(serverTimeMS)).getTime() / 1000);
       
        // Идентично модулю из index
        const post = (options) => {
            const headers = options.requestHeaders || {
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
            };
            const xhr = new XMLHttpRequest();

            xhr.onload = () => {
                if (options.success) {
                    options.success(JSON.parse(xhr.response));
                }
            };

            xhr.onloadend = () => {
                if (options.always) options.always(JSON.parse(xhr.response));
            }

            xhr.onerror = () => {
                if (options.fail) options.fail(xhr);
            }

            xhr.open('POST', options.url);

            if (options.responseType) xhr.responseType = options.responseType || 'json';

            for (let property in headers) xhr.setRequestHeader(property, headers[property]);

            xhr.send((new URLSearchParams({'data': JSON.stringify(options.data)} || 'False')).toString());
        };
        // Практически идентично тому, что в index
        // С той лишь разницей, что у данного окна разметка спинера задана явно
        const loading = new function() {
            let container;

            this.start = (containerSelector) => {
                container = document.querySelector(containerSelector);
                // Вставляем разметку спиннера в родительский контейнер
                container.insertAdjacentHTML('beforeend', `
                    <div class="modal show loading">
                        <i class="spinner icon icon--loading"></i>
                    </div>
                `);
            }
            // Удаляем из DOM
            this.end = () => {
                container.getElementsByClassName('loading')[0].remove();
            };
        };
        // Модуль отвечающий за функционал todo
        this.todo = new function() {
            // Функция, которая генерирует id для новой записи
            // По факту возвращается текущее время клиента в миллисекундах
            const generateId = () => {
                return (new Date).getTime().toString();
            };
            // Функция, которая проверяет наличие заполненности полей с датой и временем
            const checkRemind = () => {
                // Выбираем интересующие нас элементы
                const remind = document.querySelector('.remind');
                let date = document.querySelector('.date');
                let time = document.querySelector('.time');
                // Если одно из полей заполнено, то считается, что пользователь хочет создать напоминание
                if (date.value.length || time.value.length) {
                    // Если дата и время валидны
                    if (date.reportValidity() && time.reportValidity()) {
                        // Минимальное время через которое бот должен прислать напоминание
                        const minRemindTresholdS = 60; // 5 minutes
                        // Максимальное время через которое бот должен прислать напоминание
                        const maxRemindTresholdS = 31536000; // 1 year = 365 days
                        // Разбиваем строку с датой по символу точки и получаем массив с 3 элементами
                        const dateArr = date.value.split('.');
                        // Приводим к формату Месяц/День/Год для корректности интерпретации JavaScript
                        // Меняем 1 и 0 элемент массива местами и создаем строку с соединающей точкой
                        const dateMDY = ([dateArr[0], dateArr[1]] = [dateArr[1], dateArr[0]], dateArr.join('.'));
                        // Перезаписываем в переменную значение элемента вместо него самого
                        date = date.value;
                        // Перезаписываем в переменную значение элемента вместо него самого
                        time = time.value;
                        // Время в секундах через которое пользователь должен получить напоминание
                        const remindAtS = parseInt((new Date(`${dateMDY} ${time}`)).getTime() / 1000);
                        // Разница между временем напоминания и теущим временем
                        const deltaS = remindAtS - localTimeS;
                        // Если результат вписывается во временной интервал
                        if (deltaS > minRemindTresholdS && deltaS < maxRemindTresholdS) {
                            // Присваиваем класс
                            remind.className = 'todo__column remind valid';
                            // Возвращаем массив с результатами и завершаем выполнение функции
                            // Используется шаблонный литерал
                            // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Template_literals
                            return [true, deltaS, `${date} ${time}`, [dateMDY.replace(/\./g, '/'), time]];
                        }
                    }
                    // Значения даты и/или времени не валидны
                    // Присваиваем соответствующий класс
                    remind.className = 'todo__column remind invalid';
                    return [false];
                }
                // Напоминание удалено, т.е. поля с датой и временем оставлены пустыми
                remind.className = 'todo__column remind';
                return [true];
            };
            // Функция, которая перенаправляет на страницу конкретной записи для дальнейшего просмотра/редактирвоания
            this.edit = (todoId) => {
                window.location.href = '/todo?id=' + todoId;
            };
            // Функция для сохранения изменений в записи
            this.save = (todoId) => {
                loading.start('.container');
                // Проверяем поля с датой и временем
                const result = checkRemind();
                // Если поля валидны, то бишь заполнены правильно, либо пустые
                if (result[0]) {
                    const title = document.querySelector('.title').value;
                    const text = document.querySelector('.text').value;
                    const payload = { // Подготавливаем данные к отправке
                        todoId: todoId,
                        title: title,
                        text: text
                    };
                    // Если дата и время выставлены - добавляем дополнительные данные к отправке
                    if (result[1]) {
                        payload['token'] = localStorage.getItem('token');
                        payload['timeoutS'] = result[1];
                        payload['remindAt'] = result[2];
                        payload['remindAtMDYArray'] = result[3]
                    }
                    // Отправляем запрос на сервер
                    post({
                        url: '/ajax',
                        data: {
                            doAction: 'save',
                            payload: payload // Передаем данные
                        },
                        always: () => {
                            // Убираем загрузочное окно
                            loading.end();
                        }
                    });
                }
                else {
                    loading.end();
                }
            };
            // Отменяем изменения в записи, просто перезагрузив страницу и получив данные записи снова
            this.discard = (todoId) => {
                window.location.reload(true);
            };
            // Функция для удаления записи
            // Параметр todosPage - флаг, если true, то вызов происходит на странице со всем записями,
            // В противном случае - на странице конкретной записи
            this.delete = (todoId, todosPage) => {
                // Выводим загрузочное окно
                loading.start('.container');
                post({
                    url: '/ajax',
                    data: {
                        doAction: 'delete',
                        payload: { // Передаем токен с зашифрованным username, чтобы после его декодирования сервер понимал запись какого пользователя нужно удалить
                            token: localStorage.getItem('token'),
                            todoId: todoId // id Записи которуследует удалить
                        }
                    },
                    success: (response) => {
                        // Если токен декодирован и он валидный, а также данные получены
                        if (response) {
                            // Если мы на странице со всеми записями
                            if (todosPage) {
                                // Убираем запись с соответствующим id
                                document.querySelector(`[data-id="${todoId}"]`).remove();
                                // Если записей более не осталось, то присваиваем класс empty родителю
                                // Данный класс убирает ненужный padding
                                if (!(document.querySelector('.todos') || {}).innerText) {
                                    document.querySelector('.container').classList.add('empty');
                                }
                                // Завершаем выполнение функции
                                return;
                            }
                            // Запись удалена, пользователь перенаправляется на страницу со всеми записями
                            window.location.replace('/todo');
                            return;
                        }
                        // Токен более не валидный, пользователь перенаправляется на главную страницу
                        window.location.replace('/');
                    },
                    always: () => {
                        // Убираем загрузочное окно
                        loading.end();
                    }
                });
            };
            // Функция для удаления всех записей
            this.deleteAll = () => {
                loading.start('.container');
                post({
                    url: '/ajax',
                    data: {
                        doAction: 'deleteAll',
                        payload: { // Нужен только лишь токен
                            token: localStorage.getItem('token')
                        }
                    },
                    success: (response) => {
                        // Токен валидный и ответ получен
                        if (response) {
                            // Добавляем класс
                            document.querySelector('.container').classList.add('empty');
                            // Опустошаем контейнер со всеми todo
                            document.querySelector('.todos').innerText = '';
                            return;
                        }
                        // Токен более не валидный, пользователь перенаправляется на главную страницу
                        window.location.replace('/');
                    },
                    always: () => {
                        loading.end();
                    }
                });
            };
            // Функция для добавления новой записи
            this.add = () => {
                loading.start('.container');
                // Генерируем id новой записи
                const todoId = generateId();
                post({
                    url: '/ajax',
                    data: {
                        doAction: 'create',
                        payload: {
                            token: localStorage.getItem('token'),
                            todoId: todoId
                        }
                    },
                    success: (response) => {
                        // Если запись успешно создана
                        if (response) {
                            // Убираем класс empty по умолчанию всегда
                            document.querySelector('.container').classList.remove('empty');
                            const todos = document.querySelector('.todos');
                            // Добавляем разметку новой записи в DOM с динамической подстановкой переменных
                            todos.insertAdjacentHTML('afterbegin', `
                                <div class="todo" data-id="${todoId}">
                                    <span class="todo__item title"></span>
                                    <span class="todo__item text"></span>
                                    <div class="todo__item">
                                        <div class="todo__column remind" title="Time when you will be notified">
                                            <span class="label">Remind at:</span>
                                            <span class="date"></span>
                                        </div>
                                        <div class="todo__column buttons">
                                            <button class="todo__edit todo-button hover--zoom" title="Edit todo" onclick="App.todo.edit(${todoId});"><i class="icon icon--edit-todo"></i></button>
                                            <button class="todo__delete todo-button hover--zoom" title="Delete todo" onclick="App.todo.delete(${todoId}, true);"><i class="icon icon--delete-todo"></i></button>
                                        </div>
                                    </div>
                                </div>
                            `);
                        }
                    },
                    always: () => {
                        loading.end();
                    }
                });
            };
        };

        this.return = () => {
            window.location.href = '/todo';
        };

        this.logout = () => {
            localStorage.removeItem('token');
            window.location.replace('/');
        };

         // Анонимная функция такого вида будет вызвана мгновенно
         (() => {
            // Верифицируем токен на загрузке страницы
            // Достаем токен из локального хранилища
            const token = localStorage.getItem('token');
            // Если значения нет, то редиректим на главную страницу
            if (!token) {
                window.location.replace('/');
            }
            else { // Токен есть
                post({
                    url: '/ajax',
                    data: {
                        doAction: 'verifyUserToken', // Экшн/функция, которая выполнится на сервере
                        payload: {         
                            token: token
                        }
                    },
                    always: (response) => {
                        // Если токен невалидный, то редиректим на главную
                        if (response === 'invalidToken') { 
                            window.location.replace('/');
                        }
                        else { // Токен валидный, а response хранит разметку с todo
                            if (response) {
                                // Убираем класс empty у элемента с классом container
                                document.querySelector('.container').classList.remove('empty');
                                // Если контейнер todos пуст, то вставляем разметку
                                if (!document.querySelector('.todos').innerHTML && !document.querySelector('.todos').innerText) {
                                    document.querySelector('.todos').innerHTML = response;
                                }
                            }
                            // Убираем начальное загрузочное окно страницы
                            document.querySelector('.modal.loading').remove();
                        }
                    }
                });
            }

            // Каждые 2000 миллисекунды добавляет две секунды к локальному времени
            setInterval(() => {
                localTimeS += 2;
            }, 2000);
        })();
    };
};
