from aes import aes128
from base64 import b64encode, b64decode
import secrets
from loguru import logger

ALPHABET64 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
ALPHABETENUP = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
ALPHABETENLO = 'abcdefghijklmnopqrstuvwxyz'
ALPHABETSPEC = '!@#$%^&*~/*-+'
ALPHABETDIGIT = '0123456789'
ALPHABETRU = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдежзийклмнопрстуфхцчшщъыьэюя«»'

_PASSWORD = '/Zy^Qcy2X7bM$$K6'


def set_password(password: str) -> bool:
    if len(password) != 16 or not isinstance(password, str):
        logger.info('Password not set, length not equals 16!')
        return False
    else:
        global _PASSWORD
        _PASSWORD = password
        return True


def generate_password() -> str:

    alphabet = ALPHABETENUP + ALPHABETENLO + ALPHABETDIGIT + ALPHABETSPEC

    while True:
        password = ''.join(secrets.choice(alphabet) for _ in range(16))
        if (sum(c in ALPHABETDIGIT for c in password) > 2
                and sum(c in ALPHABETSPEC for c in password) > 2
                and sum(c in ALPHABETENLO for c in password) > 3):
            break

    logger.info(f"PASSWORD = '{password}'")
    return password


def normolize_alphabet_ru(text: str, tobyte: bool = True) -> str:
    """Cyrillic characters conversion to ASCII range
    from 128 to 256 as well as reverse conversion
    :param text: input text
    :param tobyte: flag transformation directions
    :return: conversion text
    """

    text_buf = []

    if tobyte:
        for ch in text:
            if ord(ch) < 128:
                text_buf.append(ch)
            elif ch in ALPHABETRU:
                text_buf.append(chr(ALPHABETRU.find(ch) + 128))
            else:
                text_buf.append(ch)
    else:
        for ch in text:
            if 127 < ord(ch) < 128 + len(ALPHABETRU):
                text_buf.append(ALPHABETRU[ord(ch) - 128])
            else:
                text_buf.append(ch)

    return ''.join(text_buf)


def encrypt(data: bytes) -> bytearray:
    step = 0
    block = [0] * 16
    crypt_data = bytearray()
    for ch in data:
        block[step] = ch
        step += 1
        if step == 16:
            crypt_data.extend(aes128.encrypt(block, _PASSWORD))
            step = 0
    else:
        if 0 < step < 16:
            for i in range(step, 15):
                block[i] = 0
            block[15] = 1
            crypt_data.extend(aes128.encrypt(block, _PASSWORD))
    return crypt_data


def decrypt(data: bytes) -> bytearray:
    step = 0
    block = [0] * 16
    crypt_data = bytearray()
    for ch in data:
        block[step] = ch
        step += 1
        if step == 16:
            crypt_data.extend(aes128.decrypt(block, _PASSWORD))
            step = 0
    return crypt_data.rstrip(b'\x00\x01')


def b64encrypt(data: str, split=79) -> str:
    data_b = normolize_alphabet_ru(data).encode('utf-8')
    # logger.debug(f'Length text {len(data)}, after encrypt85 {len(data_b)}')
    code = encrypt(data_b)
    b64 = b64encode(code).decode('utf-8')
    s_split = ['\n>>>', ]
    for start in range(0, len(b64), split):
        s_split.append(b64[start:start + split])
    s_split.append('<<<\n')
    return '\n'.join(s_split)


def b64decrypt(code: str) -> str:
    crypt_code = b64decode(code.strip('\n').encode('utf-8'))
    # logger.debug(f'Length text before decrypt85 {len(code)}, after  {len(crypt_code)}')
    if len(crypt_code) % 16 != 0:
        print('Attention: code modified. len=', len(crypt_code))
    data = decrypt(crypt_code)
    return normolize_alphabet_ru(data.decode('utf-8'), tobyte=False)


def gettextcrypt(text: str) -> str:
    if (text.find('>>>') == -1 or text.find('<<<') == -1 or
            text.find('<<<') - text.find('>>>') < 3):
        return b64encrypt(text)
    else:
        return b64decrypt(text[text.find('>>>') + 3:text.find('<<<')])
    pass


if __name__ == "__main__":
    print("Enter/Paste your content. Enter <<< for end or Ctrl-Z")
    contents = []
    status_code = False
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line == '>>>':
            status_code = True
        elif line == '<<<':
            break
        contents.append(line)

    if status_code:
        result = b64decrypt(''.join(contents))
    else:
        result = b64encrypt('\n'.join(contents))

    print(result)
    l_in = len("".join(contents))
    l_out = len(result)
    print(f'Input string length {l_in}, return length {l_out}, ratio {l_out / l_in}.')
