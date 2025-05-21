import random
import string

import bcrypt


def get_password_hash(password: str) -> str:
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    return hashed_password.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str | bytes) -> bool:
    password_byte_enc = plain_password.encode('utf-8')
    if isinstance(hashed_password, str):
        hashed_password = hashed_password.encode('utf-8')

    return bcrypt.checkpw(password=password_byte_enc, hashed_password=hashed_password)

def generate_password(length=12, use_digits=True, use_special_chars=True, use_uppercase=True):
    """
    Генерирует случайный пароль.

    Параметры:
        length (int): Длина пароля (по умолчанию 12).
        use_digits (bool): Включать цифры (0-9).
        use_special_chars (bool): Включать спецсимволы (!@#$%^&*).
        use_uppercase (bool): Включать заглавные буквы.

    Возвращает:
        str: Сгенерированный пароль.
    """
    chars = string.ascii_lowercase

    if use_uppercase:
        chars += string.ascii_uppercase
    if use_digits:
        chars += string.digits
    if use_special_chars:
        chars += "!@#$%^&*"

    password = ''.join(random.choice(chars) for _ in range(length))
    return password
