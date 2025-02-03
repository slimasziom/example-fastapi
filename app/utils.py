import bcrypt
from passlib.context import CryptContext

if not hasattr(bcrypt, '__about__'):
    bcrypt.__about__ = type('about', (object,), {'__version__': bcrypt.__version__})
pwd_context = CryptContext(schemes=["bcrypt"], deprecated='auto')


def hash(password: str):
    return pwd_context.hash(password)

def verify(plain_pwd, hashed_pwd):
    return pwd_context.verify(plain_pwd, hashed_pwd)

