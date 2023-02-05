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

    def test_normolize_alphabet_ru(self):
        from textcrypt import normolize_alphabet_ru
        text = """1 января в российских кинотеатрах состоялась премьера «Чебурашки». 
        Меньше чем за три недели сборы картины превысили 4 млрд рублей — теперь это самый кассовый фильм в истории
        российского проката. По сборам «Чебурашка» обошел предыдущих рекордсменов — первого «Аватара» и комедию
        «Холоп». Но это результаты без учета инфляции, хотя «Чебурашка» уже впереди по количеству проданных билетов.
        
        {} – этим смайликом можно продемонстрировать, что вы хотите обнять своего собеседника. :-P или :-p или :-Ъ – 
        поддразнивание собеседника высунутым языком. [:]|||[:] – изображение баяна. На интернет-сленге названием 
        этого музыкального инструмента обычно обозначают что-то уже не актуальное и много раз увиденное. 
        :-X – просьба замолчать, держать язык за зубами, взять рот на замок. /:-] – намек на то, что у собеседника
        немножко немного “чердак потек”. *:O) – символьное обозначение клоуна. Если участник переписки 
        перебрал с юмором и не может остановиться, можно его об этом уведомить.
        
        The United States government has detected and is tracking a high-altitude surveillance balloon that is 
        flying over the continental United States right now," Brig. Gen. Pat Ryder said in a statement on Thursday.
        "NORAD [North American Aerospace Defense Command] continues to track and monitor it closely.
        
        Рассказываем, почему новая история о Чебурашке заслуживает вашего внимания вне зависимости от кассовых рекордов.
        
        """
        self.assertEqual(normolize_alphabet_ru(normolize_alphabet_ru(text), tobyte=False), text)

