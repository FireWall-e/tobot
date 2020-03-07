def Main(actionName, payload, dbConfig):
    # print('KOK', doAction)
    import dataset

    db = dataset.connect(dbConfig['url'])
    print('OK')
    # return doAction(actionName, {'payload': payload, 'db': db})
    return globals()[actionName](payload, db)

def signIn(payload, db):
    table = db['users']
    user = table.find_one(login = payload['login'], password = payload['password'])
    return 'userExists' if user else 'userDoesntExist'

def signUp(payload, db):
    from functions.main import isIterable

    table = db['users']
    users = table.all()
    for user in users:
        print('db users table row is ', user)
    # print('tableis ', )
    print('payload is ', payload)
    user = db.query(
        'SELECT id FROM users WHERE email = :email OR login = :login', 
        {
            'email': payload['email'],
            'login': payload['login']
        }
    )

    if isIterable(user): 
        return 'userExists'
    else:
        table.insert({
            'email': payload['email'], 
            'login': payload['login'],
            'password': payload['password']
        })
        return 'userRegistered'
    
        

