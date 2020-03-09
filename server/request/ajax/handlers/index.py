def Main(actionName, payload, dbConfig):
    # print('KOK', doAction)
    import dataset

    db = dataset.connect(dbConfig['url'])
    print('OK')
    # return doAction(actionName, {'payload': payload, 'db': db})
    return globals()[actionName](payload, db)

def signIn(payload, db):
    table = db['users']
    users = table.all()
    for user in users:
        print('db users table row is ', user)
    user = table.find_one(username = payload['username'], password = payload['password'])
    if user:
        if 'chat_id' in user and user['chat_id']:
            from api.jwt.main import encode
            token = encode({'username': payload['username']})
            table.update({
                'username': payload['username'],
                'token': token
            }, ['username'])
            return {'message': 'validAccount', 'token': token}
        return {'message': 'invalidAccount'}
    return {'message': 'userDoesntExist'}
    # return user

def signUp(payload, db):
    from functions.main import isIterable

    table = db['users']
    users = table.all()
    for user in users:
        print('db users table row is ', user)
    # print('tableis ', )
    print('payload is ', payload)
    user = db.query(
        'SELECT id FROM users WHERE email = :email OR username = :username', 
        {
            'email': payload['email'],
            'username': payload['username']
        }
    )

    if isIterable(user): 
        return 'userExists'
    else:
        table.insert({
            'email': payload['email'], 
            'username': payload['username'],
            'password': payload['password'],
            'chat_id': '',
            'token': ''
        })
        return 'userRegistered'

def setChatIdAndToken(payload, db):
    import requests
    response = requests.get('https://api.telegram.org/bot1135448518:AAGS2SxWLmiqyDIm3cVQft4BGKHINxSw4So/getChat?chat_id=' + payload['chat_id'])
    chatExist = response.json()['ok']
    if chatExist:
        from api.jwt.main import encode
        table = db['users']
        # setUserToken(payload['username'], table)
        token = encode({'username': payload['username']})
        table.update({
            'username': payload['username'],
            'chat_id': payload['chat_id'],
            'token': token
        }, ['username'])
        return token
        

