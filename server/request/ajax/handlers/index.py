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
    return 'userExist' if user else 'userDoesntExist'

def signUp(payload, db):
    table = db['users']
    users = table.all()
    for user in users:
        print('db users table row is ', user)
    # print('tableis ', )
    print('payload is ', payload)
    user = table.find_one(email = payload['email'], login = payload['login'])
    if user: 
        return 'userExist'
    else:
        table.insert(dict(
            email = payload['email'], 
            login = payload['login'],
            password = payload['password']
        ))
        return 'userRegistered'
    
        

