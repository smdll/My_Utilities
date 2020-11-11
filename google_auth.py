# coding=utf-8
import hmac
import base64
import struct
import hashlib
import time
import random

def calGoogleCode(secretKey):
    input = int(time.time())//30
    key = base64.b32decode(secretKey)
    msg = struct.pack(">Q", input)
    googleCode = hmac.new(key, msg, hashlib.sha1).digest()
    o = googleCode[19] & 15
    googleCode = str((struct.unpack(">I", googleCode[o:o+4])[0] & 0x7fffffff) % 1000000)
    if len(googleCode) == 5:
        googleCode = '0' + googleCode
    return googleCode

def genSecretKey():
    randstr = bytearray(random.getrandbits(8) for _ in range(10))
    return base64.b32encode(randstr)

if __name__ == "__main__":
    secretKey = genSecretKey()
    print("SecretKey:", secretKey.decode())
    print("GoogleAuthCode:", calGoogleCode(secretKey))