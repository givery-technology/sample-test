__author__ = 'mizumoto'
import jwt
from datetime import datetime, timedelta

SECRET_KEY = 'adfS3WbDE580-+k64vKielnfEg23+'


def encode_token(user):
    user['exp'] = datetime.utcnow() + timedelta(days=1)
    return jwt.encode(user, SECRET_KEY, algorithm='HS256').decode()


def decode_token(token):
    try:
        options = {'verify_exp': True}
        ret = jwt.decode(token.encode(), SECRET_KEY, options=options, algorithms=['HS256'])
        return ret
    except jwt.ExpiredSignatureError:
        return None
