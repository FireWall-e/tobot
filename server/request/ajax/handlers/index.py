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
# Функция, которая отвечает за вход пользователя в систему
def signIn(payload, db):
    table = db['users']
    # Находим пользователя с полученным именем пользователя и паролем
    user = table.find_one(username = payload['username'], password = payload['password'])
    # Если пользователь зарегистрирован в системе
    if user:
        # Если пользователь уже инициировал беседу с ботом, то создаем токен
        if 'chat_id' in user and user['chat_id']:
            from api.jwt.main import encode
            # Записываем в токен имя пользователя
            # Токен будет храниться в браузере на стороне клиента
            token = encode({'username': payload['username']})
            # Записываем обновленным токен пользователя по username
            table.update({
                'username': payload['username'],
                'token': token
            }, ['username'])
    # Возвращаем результаты
            # В данном случае вернем также токен
            return {'message': 'validAccount', 'token': token}
        return {'message': 'invalidAccount'}
    return {'message': 'userDoesntExist'}
# Функция, которая отвечает за регистрацию пользователя в системе
def signUp(payload, db):
    from functions.main import isIterable

    table = db['users']
    # Находим пользователя по уникальным параметрам - email и username
    # https://dataset.readthedocs.io/en/latest/api.html#dataset.Database.query
    user = db.query(
        'SELECT id FROM users WHERE email = :email OR username = :username', 
        {
            'email': payload['email'],
            'username': payload['username']
        }
    )
    # Если пользователь - это итерируемый объект со свойствами,
    # то значит такой уже существует
    if isIterable(user): 
        return 'userExists'
    else: # В противном случае инициализируем нового пользователя в таблице
        table.insert({
            'email': payload['email'], 
            'username': payload['username'],
            'password': payload['password'],
            'chat_id': '',
            'token': ''
        })
        # Возвращаем сообщение, что пользователь успешно зарегистрирован
        return 'userRegistered'
# Функция, которая проверяет существует ли чат между пользователем и ботом,
# и в случае, если это так - создает токен и записывает это все запись пользователя
# Используется, если чат уже создан в telegram, но в БД у пользователя еще нет chat_id значения
def setChatIdAndToken(payload, db):
    import requests
    # Спрашиваем у телеграм есть ли чат
    response = requests.get('https://api.telegram.org/bot1135448518:AAGS2SxWLmiqyDIm3cVQft4BGKHINxSw4So/getChat?chat_id=' + payload['chat_id'])
    # Если ok - True, то чат существует
    chatExist = response.json()['ok']
    if chatExist:
        # Создаем токен
        from api.jwt.main import encode
        token = encode({'username': payload['username']})

        table = db['users']
        # Обновляем данные пользователя
        table.update({
            'username': payload['username'],
            'chat_id': payload['chat_id'],
            'token': token
        }, ['username'])
        # ВОзвращаем токен
        return token
        

