"""
core.py — Ядро детерминированной генерации паролей.

Алгоритм: HMAC-SHA256 + rejection sampling.
Пароль = F(master_seed, service, length, наборы_символов).

Никакой зависимости от GUI — можно использовать из консоли.
"""

import hmac
import hashlib

# Наборы символов (аналогично C#-версии, с исключением похожих: I, O, l, o)
CAPITAL = list("ABCDEFGHJKLMNPQRSTUVWXYZ")
LOWER   = list("abcdefghikmnpqrstuvwxyz")
DIGITS  = list("0123456789")
SYMBOLS = list("!@#$%&*+=-.")


def build_alphabet(use_capitals=True, use_lower=True,
                   use_digits=True, use_symbols=True) -> list[str]:
    """Собрать алфавит из выбранных наборов."""
    chars = []
    if use_capitals:
        chars.extend(CAPITAL)
    if use_lower:
        chars.extend(LOWER)
    if use_digits:
        chars.extend(DIGITS)
    if use_symbols:
        chars.extend(SYMBOLS)
    return chars


def generate_password(
    master_seed: str,
    service: str,
    length: int,
    use_capitals: bool = True,
    use_lower: bool = True,
    use_digits: bool = False,
    use_symbols: bool = True,
) -> str:
    """
    Детерминированная генерация пароля.

    Параметры:
        master_seed — мастер-фраза (то, что пользователь держит в голове)
        service     — название сервиса (google, vk, …)
        length      — длина пароля
        use_*       — какие наборы символов разрешены

    Возвращает:
        строку-пароль

    Бросает:
        ValueError — если master_seed пуст или не выбран ни один набор символов
    """
    if not master_seed:
        raise ValueError("Сид-фраза не может быть пустой")

    alphabet = build_alphabet(use_capitals, use_lower, use_digits, use_symbols)
    if not alphabet:
        raise ValueError("Должен быть выбран хотя бы один набор символов")

    alphabet_len = len(alphabet)
    # Максимальное значение байта, дающее равномерное распределение
    max_valid = 256 - (256 % alphabet_len)

    key = master_seed.encode("utf-8")
    # message = service + length — чтобы длина влияла на пароль
    msg_base = f"{service}{length}".encode("utf-8")

    password: list[str] = []
    counter = 0

    while len(password) < length:
        msg = msg_base + bytes([counter])
        digest = hmac.new(key, msg, hashlib.sha256).digest()

        for byte in digest:
            if byte < max_valid:
                password.append(alphabet[byte % alphabet_len])
                if len(password) == length:
                    break
        counter += 1

    return "".join(password)
