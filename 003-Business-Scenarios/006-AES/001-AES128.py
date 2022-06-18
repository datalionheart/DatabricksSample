# Databricks notebook source
plaintext = "4fcb4d893a2e007f74c51ca2e4091950b17a1e574828cf665b06c5a61d0532c892df36b1c9155edf40d7c571f99dbdea71f6a9956fc770fc33e8ac9c413ef1042d8a38de41196175c954a50b1d3589220eedbe46a0496ba836db9b994c8abbb85dccde865e29419100b9d54723fd1c4c6e1395e7e03c4ccfb0ea3de053a5c15425441bbe13b018d429e4488df930676ba023da322ea5de841d6cb50a41407a7cb00943c1ba2c0692bb79b55d78563e8d7030941daf66d63a46b1699414149acd186c60a43e56c1b4b6d9356ff2202256257719a7e149e445d2eb073920c6cf882ae1ff42df815accb130cfeb9b6e6fcf448bbdf6f62a1891a66e43356c4231b3a8e296a5192ba5719de6c52578663a884d0e08d6f44f5d421dab9c0d10a0a47d4d39072699afbc24061f03906ad9c588"

# COMMAND ----------

key = "051de7059b4e404b"

# COMMAND ----------

import binascii
import re
from Crypto.Cipher import AES
 
class AESCBC:
    def __init__(self):
        self.key = '051de7059b4e404b'            #定义key值
        self.mode = AES.MODE_ECB
        self.bs = 16  # block size
        self.PADDING = lambda s: s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)
 
    def encrypt(self, text):
        generator = AES.new(self.key, self.mode,self.key)    #这里的key 和IV 一样 ，可以按照自己的值定义
        crypt = generator.encrypt(self.PADDING(text))
        # crypted_str = base64.b64encode(crypt)   #输出Base64
        crypted_str =binascii.b2a_hex(crypt)       #输出Hex
        result = crypted_str.decode()
        return result
 
    def decrypt(self, text):
        generator = AES.new(self.key, self.mode,self.key)
        text += (len(text) % 4) * '='
        # decrpyt_bytes = base64.b64decode(text)           #输出Base64
        decrpyt_bytes = binascii.a2b_hex(text)           #输出Hex
        meg = generator.decrypt(decrpyt_bytes)
        # 去除解码后的非法字符
        try:
            result = re.compile('[\\x00-\\x08\\x0b-\\x0c\\x0e-\\x1f\n\r\t]').sub('', meg.decode())
        except Exception:
            result = '解码失败，请重试!'
        return result
 
 
if __name__ == '__main__':
    aes = AESCBC()
 
    to_encrypt = '123456'
    to_decrypt = '32331c5e8a96e2fb4d2c04d33452a2d2e87da67a8920e012c5db04290138bd4725b6e93b876a6d68f29cd1190081db1671f6a9956fc770fc33e8ac9c413ef1042d8a38de41196175c954a50b1d3589220eedbe46a0496ba836db9b994c8abbb8c05b440e5291aa3174c85d711fe291ea6e1395e7e03c4ccfb0ea3de053a5c1546cc4e85b3c1f84a212e98c68a0c281b0c9c7051abbd61245cb23406a7b0ac9b0b00943c1ba2c0692bb79b55d78563e8d7030941daf66d63a46b1699414149acd186c60a43e56c1b4b6d9356ff2202256257719a7e149e445d2eb073920c6cf88b1f3d615166dc758ad18c51eeb834bb7b577ce1ff737580e7748011cf9e98801f3b4082fec386a6071551082b7b133bc2abe55d669bc0d54b84373fd4111841bd7c0001de1f3a29fbddfcb6557526ecc'
 
    print("\n加密前:{0}\n加密后：{1}\n".format(to_encrypt,aes.encrypt(to_encrypt)))
    print("解密前:{0}\n解密后：{1}".format(to_decrypt,aes.decrypt(to_decrypt)))