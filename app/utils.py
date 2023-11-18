from passlib.context import CryptContext

hashing = CryptContext(schemes=['bcrypt'], deprecated='auto')


def strong_password(password: str):
    return hashing.hash(password)