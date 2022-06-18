# Databricks notebook source
# MAGIC %md
# MAGIC Install library pycrypto from PyPI to cluster

# COMMAND ----------

key = "051de7059b4e404b"
plaintext = "SQL Server 2022 (16.x) Preview builds on previous releases to grow SQL Server as a platform that gives you choices of development languages, data types, on-premises or cloud environments, and operating systems."
ciphertext = "72e75be85b638949c9b09d6c85e6401f18d93643c50c573c55ba1856fa99fa39b7dd3af2f70a2522b7e4dec530dc42732a732a8b34c6667173367fef2811d0df7461bd5762eabc8a53e8e749ddb307a5f47851d5bd3c221c92868db6f4887aa4f62a805c6925716212eddba9e38607e94e40a0abc3577ee6746c8e829ec3444b996809e4705515e7629a1ff8eb45c0a4cda60fd858152ab6aec0389d1240f91f7eb0b881041e3a91cc071a163a56034523e3d67af03389ed696915245f28a0229c0c74af5cde3a6caa9cf6117e52667fd0f2e475678433570b787c76b52718b6"

# COMMAND ----------

import binascii
import re
from Crypto.Cipher import AES
 
class AESECB:
    def __init__(self):
        self.key = key                                       # Defined key value
        self.mode = AES.MODE_ECB                             # Used encryption algorithm
        self.bs = 16  # block size: AES128 16/ AES 256 32
        self.PADDING = lambda s: s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)
 
    def encrypt(self, text):
        generator = AES.new(self.key, self.mode,self.key)    # IV same with key
        crypt = generator.encrypt(self.PADDING(text))
        # crypted_str = base64.b64encode(crypt)              # Output Base64
        crypted_str =binascii.b2a_hex(crypt)                 # Output Hex
        result = crypted_str.decode()
        return result
 
    def decrypt(self, text):
        generator = AES.new(self.key, self.mode,self.key)
        text += (len(text) % 4) * '='
        # decrpyt_bytes = base64.b64decode(text)             # Output Base64
        decrpyt_bytes = binascii.a2b_hex(text)               # Output Hex
        meg = generator.decrypt(decrpyt_bytes)
        # Remove illegal characters after decoding
        try:
            result = re.compile('[\\x00-\\x08\\x0b-\\x0c\\x0e-\\x1f\n\r\t]').sub('', meg.decode())
        except Exception:
            result = 'Decrpyt failed.'
        return result
 
 
if __name__ == '__main__':
    aes = AESECB()
 
    to_encrypt = plaintext
    to_decrypt = ciphertext
 
    print(aes.encrypt(to_encrypt))
    print(aes.decrypt(to_decrypt))