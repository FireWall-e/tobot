// Нижеприведенный код выполнится после загрузки окна браузера - window.onload
window.onload = () => {
    // Создаем объект App и записываем в глобальную переменную window
    // Об использовании ключевого слова this изложено по следующей ссылке
    // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/this
    // tl;dr this привязан к контексту выполнения т.е. в случае с this.App, под
    // this подразумевается window, который находится выше по скоупу/зоне видимости (scope)
    // Все методы с использованием this в данном примере являются публичными, 
    // То есть доступны для вызова из DOM https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model
    // Для примера можно взять атрибут onclick, которому как значение передан метод, который должен быть вызван
    // в данном случае при клике, например, onclick="App.something.doSomething()"
    this.App = new function() {

        // Модуль модального окна
        const modal = function () {
            // Фукнция создания модального окна, которая принимает
            // дополнительный кастомный класс и параметр-флаг clickToRemove
            // если true, то модалку моужно будет закрыть просто кликнув по нему
            this.create = (customClassname = '', clickToRemove = false) => {
                // Класс модалки
                const className = customClassname ? 'modal ' + customClassname : 'modal';
                // Если модалка с таким классом уже используется, 
                // то завершаем выполнение функции фразой return;
                if (document.querySelector('.' + className.trim().replace(/\s/g, '.'))) return;
                this.modal = document.createElement('div');
                this.modal.className = className;
                // Если применяется закрытие по клику, то присваиваем дополнительные свойства
                if (clickToRemove) {
                    this.modal.style.cursor = 'pointer';
                    this.modal.addEventListener('click', this.modal.remove);
                    this.modal.title = 'Click on me to close';
                }
            };
            // Метод, который отвечает за добавления контента в модалку
            this.addContent = (content, position = 'beforeEnd') => {
                // Если передана строка, то используем insertAdjacentHTML
                if (typeof content === 'string') {
                    // https://developer.mozilla.org/en-US/docs/Web/API/Element/insertAdjacentHTML
                    this.modal.insertAdjacentHTML(position, content);
                }
                else { // В данном случае подразумевается что передан какой-либо html элемент
                    // https://developer.mozilla.org/en-US/docs/Web/API/ParentNode/append
                    this.modal.append(content);
                }
            };
            // Удаляет контент модалки
            this.removeContent = () => {
                this.modal.innerHTML = '';
            };
            // Отвечает за добавление модалки в DOM
            // Аргумент container определяет родителя в которого будет помещена модалка
            this.pushIn = (container) => {
                // Записываем в переменную модалки
                // для дальнейшего использования внутри других методов модалки
                this.container = container;
                // Добавляем класс show, который делает модалку видимой
                this.modal.classList.add('show');
                // Добавляем модалку внутрь родительского контейнера
                container.append(this.modal);
            };
            // Прячет модалку, но не убирает ее из DOM
            this.hide = (removeContent = false) => {
                this.modal.classList.remove('show');
                if (removeContent) this.removeContent();
            };
            // Удаляет из DOM
            this.remove = () => {
                this.modal.remove();
            };
        };
        // Модуль загрузочного окна
        const loading = function (container) {
            // Создаем элемент загрузочный спинер
            const spinner = document.createElement('i');
                  spinner.className = 'spinner icon icon--loading';
            // Используем модуль модального окна
            const loadingModal = new modal();
            // Создаем модальное окно загрузки
                  loadingModal.create();

            // Выводит/запускает загрузочное окно
            this.start = () => {
                // Убираем фокус с активного элемента
                document.activeElement.blur();
                // Добавляем спиннер в загрузочное окно
                loadingModal.addContent(spinner);
                // Помещаем его внутрь родителя - container
                loadingModal.pushIn(container);
            };
            // Вызывается при окончании загрузки
            // Удаляет загрузочное окно из dom
            this.end = () => {
                loadingModal.remove();
            };
        };
        // Модуль осуществления пост запросов
        // По факту это обертка для нативного api XMLHttpRequest
        const post = (options) => {
            // Переменная с заголовками запроса
            const headers = options.requestHeaders || {
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
            };
            // Создаем новый экзэмпляр XMLHttpRequest
            const xhr = new XMLHttpRequest();
            // Функция, которая обрабатывает завершенные запросы
            xhr.onload = () => {
                // Если была передана функция обработчик           
                if (options.success) {
                    // Вызываем ее, предварительно преобразовав json строку с ответом - xhr.response в объект 
                    options.success(JSON.parse(xhr.response));
                }
            };
            // Функция, которая срабатывает после отправки запроса
            xhr.onloadend = () => {
                // Если была передана функция обработчик
                // Возвращаем целый xhr объект
                if (options.always) options.always(xhr);
            }
            // Функция, которая обрабатывает ошибки запроса
            xhr.onerror = () => {
                // Если была передана функция обработчик
                // Возвращаем целый xhr объект
                if (options.fail) options.fail(xhr);
            }
            // Начинаем отправку POST запроса
            xhr.open('POST', options.url);
            // Ожидаемый тип данных ответа, которые будут получены от сервера
            // По умолчанию 'json'
            if (options.responseType) xhr.responseType = options.responseType || 'json';
            // Устанавливаем заголовки
            for (let property in headers) xhr.setRequestHeader(property, headers[property]);
            // Отправляем запрос преобразовывая передаваемые данные с использование URLSearchParams
            // https://developer.mozilla.org/en-US/docs/Web/API/URLSearchParams
            xhr.send((new URLSearchParams({'data': JSON.stringify(options.data)} || 'False')).toString());
        };
        // Динамически показываем слайд, добавляя соответствующий класс вида 'show-slide-' + name 
        // элементу document.querySelector('.content'), то бишь с классом content
        // О селекторах подробнее тут https://www.w3schools.com/w3js/w3js_selectors.asp
        const showSlide = (name) => {
            return () => {
                document.querySelector('.content').classList.add('show-slide-' + name);
            }
        };
        // Скрываем слайд, убирае соответствующий класс
        const hideSlide = (name) => {
            return () => {
                document.querySelector('.content').classList.remove('show-slide-' + name);
            }
        };
        // Функция, которая экранирует двойные кавычки
        // Используется, чтобы избежать ошибок форматирования строк
        // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String#Escape_notation
        const escapeQuotes = (string) => {
            return string.replace(/"/g, '\\"');
        };
        // Модуль для создания дополнительно "элемента-маски", который используется
        // Для вывода дополнительного окна при нативной html валидации форм
        // https://developer.mozilla.org/en-US/docs/Learn/Forms/Form_validation
        const bindValidityMask = (form, targetSelector, message, focusAfter) => {
            // target - переменная константа, которая хранит элемент к которому будет применена маска
            const target = document.querySelector(targetSelector);
            // Если хотим возвращать фокус полю после на событии keypress
            if(focusAfter === 'keypress') {
                // Возвращает фокус элементу при нажатии любой клавиши
                const keypressHandler = () => {
                    target.focus();
                    e.currentTarget.removeEventListener(e.type, keypressHandler);
                }
                // "Вешаем" обработчик события элементу document
                document.addEventListener('keypress', keypressHandler);
            }
            // Если элемент уже содержится в DOM, то запишет ее в переменную, в противном случае - undefined
            const maskElementExist = document.querySelector('[data-mask-for-selector="' + escapeQuotes(targetSelector) + '"]');
            // Если элемент уже содержится в DOM, то возвращаем его и завершаем дальнейшее выполнение функции
            if(maskElementExist) return maskElementExist;
            // Получаем данные о расположении целевой формы (в пикселях)
            const formCoordinates = form.getBoundingClientRect();
                  form.style.position = 'relative'; // Добавляем стиль позиционирования
            // Получаем координаты цели (в пикселях)
            const targetCoordinates = target.getBoundingClientRect();
            // Создаем маску и настраиваем ее
            const mask = document.createElement('input');
                  mask.setAttribute('required', 'true');
                  mask.setAttribute('pattern', '.{}');
                  mask.setAttribute('autocomplete', 'off');
                  mask.setAttribute('autocorrect', 'off');
                  mask.setAttribute('spellcheck', 'false');
                  mask.dataset.maskForSelector = targetSelector;
                  mask.setCustomValidity(message);
                  mask.className = "validity-mask";
                  mask.style.zIndex = -999;
                  mask.style.position = 'absolute';
                  mask.style.color = 'transparent';
                  mask.style.width = targetCoordinates.width + 'px';
                  mask.style.left = (targetCoordinates.x - formCoordinates.x) + 'px';
                  mask.style.top = (targetCoordinates.y - formCoordinates.y) + 'px';
            // Можно возвращать фокус элементу по истечении 1.5 секунд, или 1500 мс
            if(focusAfter === 'timeout') {
                // Возвращаем фокус на событии invalid, где e - переменная, которая хранит данные события
                mask.addEventListener('invalid', (e) => {
                    setTimeout(()=>target.focus(), 1500);
                });
            }
            // Добавляем созданную маску в форму
            form.appendChild(mask);
            // Возвращаем созданную маску
            return mask;
        };
        // Функция для проверки валидности полей формы
        const htmlCheckValidity = (form) => {
            // В цикле перебераем дочерние элементы формы
            for (let i = 0; i < form.children.length; i++) {
                const item = form.children.item(i);
                // Если это маска, то переходим к следующей итерации / дочернему элементу
                if(item.dataset.maskForSelector) continue;
                // https://developer.mozilla.org/en-US/docs/Web/API/HTMLFormElement/reportValidity
                if(!item.reportValidity()) return false; // Если не прошел валидацию хотя бы 1 элемент формы, то
                // Завершаем выполнение функции возвращая false
            }
            // Все элементы успешно прошли валидацию
            return true;
        }
        // Функция для обработки формы
        const proceedForm = (event, form, optional) => {
            // Останавливаем дефолтный сценарий выполнения события
            // https://developer.mozilla.org/en-US/docs/Web/API/Event/preventDefault
            event.preventDefault();
            // Если не передана функция для дополнительной кастомной валидации создаем пустышку - optional.customValidate = ()=>true
            !optional.customValidate && (optional.customValidate = ()=>true);
            // Если не передана функция, которая будет вызвана, если валидация не прошла - создаем пустышку
            !optional.oninvalid && (optional.oninvalid = ()=>true);
            // Если форма прошла валидацию
            if (htmlCheckValidity(form)) {
                // Сериализуем форму
                // https://developer.mozilla.org/en-US/docs/Web/API/FormData
                const formData = new FormData(form);
                const resultFormData = {}; // Пустая переменная для записи результата
                
                // Проходимся по каждомо элементу формы
                for (let [name, value] of formData.entries()) { 
                    // И записываем в результирующий объект
                    resultFormData[name] = value;
                }
                // Если дополнительная кастомная валидация пройдена, то вызываем обработчик onvalid
                // В противном случае - oninvalid
                // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Conditional_Operator
                return optional.customValidate(resultFormData) 
                       ? optional.onvalid(resultFormData) 
                       : optional.oninvalid();
            }
            // Функция, которая будет вызвана если функция не валидна
            return optional.oninvalid();
        };
        // Модуль логина
        this.signIn = new function() {
            // Класс - селектор
            const selector = 'sign-in';
            // Используем декоратор showSlide для показа слайда
            // Куда передаем селектор
            this.showForm = showSlide(selector);
            // Используем декоратор hideSlide для сокрытия слайда
            // Куда передаем селектор
            this.hideForm = hideSlide(selector);
            // Функция, которая вызывается по нажатию для отправки формы
            this.submitForm = (event) => {
                const form = document.querySelector('.' + selector + '__form');
                const container = document.querySelector('.content');
                // Выводим загрузку
                const loadingSpin = new loading(container);
                      loadingSpin.start();
                // Вызываем обработчик формы
                proceedForm(event, form, {
                    onvalid: (formData) => { // Если форма валидна
                        // Совершаем пост запрос, в теле которого передаем данные формы
                        post({
                            url: '/ajax', // относительный путь; куда будет отправлен запрос. Пример полного - 127.0.0.1/ajax
                            data: {
                                doAction: 'signIn', // Функция/действие которое будет вызвано на сервере для обработки запроса
                                payload: { // Передаваемы данные
                                    username: formData.username,
                                    password: formData.password
                                } 
                            }, // Функция, которая будет вызвана, если запрос успешно отправлен и ответ от сервера получен
                            success: (response) => {
                                // Создаем модалку, которая будет содержать ответ клиенту на отправленный запрос
                                const responseModal = new modal();
                                      responseModal.create('sign-in-modal', true);
                                // Если ответ валидный
                                if (response.message === 'validAccount') {
                                    // Записываем токен в локальное хранилище
                                    // https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage
                                    localStorage.setItem('token', response.token);
                                    // Редеректим на внутреннюю страницу со всеми todo
                                    window.location.replace('/todo');
                                } // Если такого пользователя не существует
                                else if (response.message === 'userDoesntExist') {
                                    // Добавляем следующее сообщение в модалку
                                    responseModal.addContent(`
                                        User with such account data doesnt exist!
                                    `);
                                    // Выводим модалку
                                    responseModal.pushIn(container);
                                } // Если пользователь существует, но у него не настроен чат с ботом
                                else if (response.message === 'invalidAccount') {
                                    post({ // Отправляем запрос к telegram api, т.к. возможно чат существует, но в БД поле пустое
                                        url: 'https://api.telegram.org/bot1135448518:AAGS2SxWLmiqyDIm3cVQft4BGKHINxSw4So/getUpdates',
                                        success: (response) => { // Получаем ответ
                                            // Если за последние 24 часа существует история всех сообщений адресованных боту
                                            if (response.result.length) {
                                                // Если есть сообщение от пользователя с соответствующим username, то записываем в переменную
                                                const messageItem = response.result.find(messageItem => messageItem.message.from.username === formData.username);
                                                // Если сообщение валидно, то отправляем запрос серверу
                                                // Чтобы он записал chat_id в строку с соответствующим username
                                                if (messageItem) {
                                                    post({
                                                        url: 'ajax',
                                                        data: {
                                                            doAction: 'setChatIdAndToken',
                                                            payload: {
                                                                username: formData.username,
                                                                chat_id: messageItem.message.chat.id.toString()
                                                            }
                                                        },
                                                        success: (token) => {
                                                            // Запрос прошел успешно и получен token
                                                            if (token) {
                                                                // Записываем в локальное хранилище
                                                                localStorage.setItem('token', token);
                                                                // Редиректим на внутреннюю страницу со всеми todo
                                                                window.location.replace('/todo');
                                                                // Прерываем дальнейшее выполнение функции
                                                                return;
                                                            }
                                                            // Ошибка обработки запроса, выводи соответствующее сообщение
                                                            responseModal.addContent(`
                                                                An error occured, please try again later :(
                                                            `);
                                                            responseModal.pushIn(container);
                                                        },
                                                        fail: () => { // Запрос вообще не был обработан сервером
                                                            responseModal.addContent(`
                                                                Sorry, service temporary unavailable :(
                                                            `);
                                                            responseModal.pushIn(container);
                                                        },
                                                        always: () => { // Выполняем всегда
                                                            // Убираем окно загрузки
                                                            loadingSpin.end();
                                                        }
                                                    });
                                                    // Прерываем дальнейшее выполнение функции
                                                    return;
                                                }
                                            }
                                            // Убираем окно загрузки
                                            loadingSpin.end();
                                            // Чат между ботом и пользователем не существует,
                                            // выводим соответствующее сообщение с просьбой инициализировать чат
                                            responseModal.addContent(`
                                                Please make a friendship with <a href="https://telegram.me/pros_tobot?start" target="_blank title="I am available 24/7"> Tobot</a> :)
                                            `);
                                            responseModal.pushIn(container);
                                        },
                                        fail: () => { // Телеграм не обработал запрос
                                            loadingSpin.end();
                                            responseModal.addContent(`
                                                Sorry, telegram's service temporary unavailable :(
                                            `);
                                            responseModal.pushIn(container);
                                        }
                                    });
                                    return;
                                }
                                loadingSpin.end();
                                form.reset(); // Опустошаем заполненные поля формы
                            }
                        });
                    },
                    oninvalid: () => { // Если форма не прошла валидацию
                        loadingSpin.end();
                    }
                });
            };
        };
        // Модуль регистрации
        this.signUp = new function() {
            const selector = 'sign-up';
            // Функция валидации паролей
            const validatePasswords = (formData, passwordRepeatMask) => {
                // Если подтвержденный (второй) пароль не совпадает с первым
                if(formData.password !== formData.passwordRepeat) {
                    passwordRepeatMask.reportValidity();
                    return false;
                }
                // Оба пароля валидны
                // Удаляем маску пароля
                passwordRepeatMask.remove();
                return true;
            };
            // Декораторы
            this.showForm = showSlide(selector);
            this.hideForm = hideSlide(selector);
            // Механизм аналогичный модулю логина
            // Подтверждаем отправку формы
            this.submitForm = (event) => {
                const container = document.querySelector('.content');
                const loadingSpin = new loading(container);
                      loadingSpin.start();
                const form = document.querySelector('.' + selector + '__form');
                // Обрабатываем форму
                proceedForm(event, form, {
                    customValidate: (formData) => { // Добавляем кастомную дополнительную валидацию паролей
                        const passwordRepeatMask = bindValidityMask(
                            form, 
                            'input[name="passwordRepeat"]',
                            'Passwords should be identical!',
                            'timeout'
                        );
                        // Оба поля с паролями должны совпадать
                        // Возвращаем результат валидации паролей
                        return validatePasswords(formData, passwordRepeatMask);
                    },
                    onvalid:  (formData) => { // Форма валидна
                        // Отправляем запрос на регистрацию пользователя
                        post({
                            url: '/ajax',
                            data: {
                                doAction: 'signUp',
                                payload: { // Отправляем данные пользователя
                                    email: formData.email,
                                    username: formData.username,
                                    password: formData.password
                                }
                            },
                            success: (response) => {
                                // Создаем заготовку модального окна для ответа пользователю на отправленный запрос
                                const responseModal = new modal();
                                      responseModal.create('sign-up-modal', true);
                                // Пользователь с таким email или username уже зарегистрирован
                                if (response === 'userExists') {
                                    // Добавляем соответствующее сообщение
                                    responseModal.addContent(`
                                        <div class="modal__item">
                                            User already exists!
                                        </div>
                                    `);
                                } // Пользователь успешно зарегистрирован
                                else if (response === 'userRegistered') {
                                    // Выводим сообщение с ссылкой: с настройкой чата между пользователем и ботом
                                    responseModal.addContent(`
                                        <div class="modal__item">
                                            Registration completed! <br/>
                                            Just one more step left! <br/>
                                            Folow this link to setup your <a href="https://telegram.me/pros_tobot?start" target="_blank title="Click on me to start our friendship">Tobot</a> :)
                                        </div>
                                    `);
                                }
                                // Выводим модалку
                                responseModal.pushIn(container);
                                form.reset(); // Опустошаем данные формы
                            },
                            always: () => {
                                loadingSpin.end();
                            }
                        });
                    },
                    oninvalid: () => { // Форма не прошла валидацию и не была отправлена
                        loadingSpin.end();
                    }
                });
            };
        };

        // Модуль "О проекте"
        this.about = new function() {
            // Декораторы
            this.show = showSlide('about');
            this.hide = hideSlide('about');
        };
    };
};