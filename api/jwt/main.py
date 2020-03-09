import jwt

JWT_SECRET = '8~\^bvh856/j[ecGP!nK}eMvvamNWc7R'
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = 86400

def encode(payload):
    from datetime import datetime,timedelta
    payload['exp'] = datetime.utcnow() + timedelta(seconds = JWT_EXP_DELTA_SECONDS)
    token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)
    return token.decode('utf-8')

def decode(token):
    try:
        return jwt.decode(token, JWT_SECRET, JWT_ALGORITHM)
    except jwt.ExpiredSignatureError:
        return False
