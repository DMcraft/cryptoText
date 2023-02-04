from aes import aes128
from base64 import b64encode, b64decode
import random
from loguru import logger

ALPHABET64 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
ALPHABETEN = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
ALPHABETRU = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдежзийклмнопрстуфхцчшщъыьэюя'

_PASSWORD = 'JHF6d2@0LK#skK$l'


def set_password(password: str) -> bool:
    if len(password) != 16 or not isinstance(password, str):
        logger.info('Password not set, length not equals 16!')
        return False
    else:
        global _PASSWORD
        _PASSWORD = password
        return True


def generate_password() -> str:
    buf = []
    for _ in range(16):
        buf.append(random.choice(ALPHABET64))
    logger.info(f"PASSWORD = '{''.join(buf)}'")
    return ''.join(buf)


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
        if 0 < step < 15:
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
    data_b = data.encode('utf-8')
    # data_b += (' ' * (16 - len(data_b) % 16)).encode('utf-8')
    code = encrypt(data_b)
    b64 = b64encode(code).decode('utf-8')
    s_split = ['\n>>>', ]
    for start in range(0, len(b64), split):
        s_split.append(b64[start:start + split])
    s_split.append('<<<\n')
    return '\n'.join(s_split)


def b64decrypt(code: str) -> str:
    crypt_code = b64decode(code.strip('<>\n').encode('utf-8'))
    if len(crypt_code) % 16 != 0:
        print('Attention: code modified. len=', len(crypt_code.decode('utf-8')))
    data = decrypt(crypt_code)
    return data.decode('utf-8')


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