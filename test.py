from textcrypt import *
from loguru import logger

table = (
            ('Привет, приветб сосед соединил буфет с комодом в среду!!!',
             '\n>>>\nWHPNIUh1A6T2nWVMEPtGq1mtTRHwms0/Y9vRfA/ULlkDZ+CId1ElSAAb1orrl5a8YrTuFUzvAD3Fo1a'
             '\n1KOxIaOyw/bqGOxrKdB5YD0HiAKXyWCyBhr7yhnlTUTi/6HDdKkC7v41mS2hb6v8HNuN0FA==\n<<<\n'),
            ('123rty123tyu',
             '\n>>>\nErkobRBul6DCsWRUcmo2wA==\n<<<\n'),
            ('asdfghqwerty12387dlkointvqmpveohnclasdafhn;lsadnjdsclaksd',
             '\n>>>\nWWjmyNtYGRGkC+GZ2XgqrbJENxX0J/4u+yFBM/Viit/LTXFHrP1SO+JKHnLROkh/3nGFauYikLPhhMh'
             '\nDlVcVrQ==\n<<<\n')
         )


logger.info("Start test")
for text, code in table:
    print(text)
    print(b64encrypt(text))
    print(b64decrypt(b64encrypt(text)))
    print('>>')

print(decrypt(encrypt(';lsdkfjg;lakjsgvasdfgvaadfvadfvadfvadfv'.encode('utf-8'))).decode('utf-8'))


