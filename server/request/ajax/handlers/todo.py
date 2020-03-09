def Main(actionName, payload, dbConfig):
    # print('KOK', doAction)
    import dataset

    db = dataset.connect(dbConfig['url'])
    # print('OK')
    # return doAction(actionName, {'payload': payload, 'db': db})
    return globals()[actionName](payload, db)

def verifyUserToken(payload, _):
    from api.jwt.main import decode
    encryptedPayload = decode(payload['token'])
    # print('token is ', ecryptedPayload)
    return 'true' if encryptedPayload else ''

def createTodo(payload, db):
    table = db['todos']
    rowId = table.insert({
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