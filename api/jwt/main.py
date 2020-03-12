# Библиотека для работы с json web токенами
import jwt

# Секрет, необходимый при decode и encode токена
JWT_SECRET = '8~\^bvh856/j[ecGP!nK}eMvvamNWc7R'
# Алгоритм для шифрования данныз при encode
JWT_ALGORITHM = 'HS256'
# Время жизни токена в секундах
JWT_EXP_DELTA_SECONDS = 86400

# Шифрует полученные данные и записывает в токен
def encode(payload):
    # Библиотеки для работы со временем
    from datetime import datetime,timedelta
    # Время истечения токена
    payload['exp'] = datetime.utcnow() + timedelta(seconds = JWT_EXP_DELTA_SECONDS)
    # Генерируем токен
    token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)
    # Возвращаем сгенерированный токен в кодировке utf-8
    return token.decode('utf-8')

# Декодируем токен, то есть достаем данные из токена,
# в случае если токен еще не просрочился/испортился (jwt.ExpiredSignatureError)
def decode(token):
    try: # Декодируем
        return jwt.decode(token, JWT_SECRET, JWT_ALGORITHM)
    except jwt.ExpiredSignatureError:
        return False # Возвращаем False, если токен просрочился/испоритлся
