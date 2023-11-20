from passlib.context import CryptContext

hashing = CryptContext(schemes=['bcrypt'], deprecated='auto')


def strong_password(password: str):
    return hashing.hash(password)


def verify_password(plain_password, hashed_password):
    return hashing.verify(plain_password, hashed_password)
