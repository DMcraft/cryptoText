from unittest import TestCase


class Test(TestCase):
    def test_set_password(self):
        from textcrypt import set_password
        self.assertEqual(set_password('12345'), False)
        self.assertEqual(set_password('1234567890qwerty'), True)

    def test_generate_password(self):
        from textcrypt import generate_password
        self.assertEqual(len(generate_password()), 16)

    def test_crypt(self):
        from textcrypt import encrypt, decrypt
        text = ('I am not big style duck..'.encode('utf-8'),
                'I am not большая утка..'.encode('utf-8'),
                'Есть в мире много всякого разного!'.encode('utf-8'))
        for t in text:
            self.assertEqual(decrypt(encrypt(t)), t)

    def test_b64crypt(self):
        from textcrypt import b64encrypt, b64decrypt
        text = ('I am not big style duck..',
                'I am not большая утка..',
                'Есть в мире много всякого разного!')
        for t in text:
            self.assertEqual(b64decrypt(b64encrypt(t)), t)





