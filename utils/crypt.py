import random
import base64
import uuid
import bcrypt
from utils.text import force_bytes


def hashpw(password):
    return bcrypt.hashpw(force_bytes(password), bcrypt.gensalt())


def checkpw(password, hashed_pw):
    return bcrypt.checkpw(force_bytes(password), force_bytes(hashed_pw))


def gen_cookie_secret():
    return base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)


def get_random_string(length=12,
                      allowed_chars='abcdefghijklmnopqrstuvwxyz'
                                    'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'):

    return ''.join(random.choice(allowed_chars) for _ in range(length))
