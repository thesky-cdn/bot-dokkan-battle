'''
Modification of https://github.com/FlashChaser/Open-Source-Battle-Bot/blob/development/packet.py
done to support multiple accounts at once via a discord bot.
crypto.py is vital functions used for data encryption/decryption in dokkan web API requests.
'''
import base64
import binascii
import config
from Crypto.Cipher import AES
import hashlib
import hmac
import json
import os
import time
import uuid

# Padding for the input string --not
# related to encryption itself.
BLOCK_SIZE = 16  # Bytes
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE
        - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]
####################################################################
def guid():
    UUID = str(uuid.uuid4())
    UniqueId = str(uuid.uuid4()) + ':' + UUID[0:8]
    return [str(uuid.uuid4()), UniqueId]
####################################################################
def basic(identifier):
    #remove next-lines
    if '\n' in identifier:
        temp = identifier.replace('\n', '')
    else:
        temp = identifier
    #append blanks to make size of 160
    if len(temp) < 159:
        while len(temp) < 159:
            temp = temp.ljust(159, '\u0008')
    #flip identifier
    decode = base64.b64decode(temp).decode()
    part = decode.split(':')
    temp = part[1] + ':' + part[0]
    #basic
    basic = base64.b64encode(temp.encode()).decode()
    return basic
####################################################################
'''
this specific def is written by k1mpl0s with assistance of renzy.
the one written by flashchaser was very flawed & not up to date.
flaw example: nonce in packets are clearly a md5 hash but in flashes code it uses a UUID, signature is malformed in flashes code.
'''
def mac(ver, token, secret, method, endpoint):
    if ver == 'gb':
        host = config.gb_url.replace('https://', '').split(':')[0]
        port = config.gb_port
    else:
        host = config.jp_url.replace('https://', '').split(':')[0]
        port = config.jp_port
    ts = str(int(round(time.time(), 0)))
    nonce = ts + ':' + str(hashlib.md5(ts.encode()).hexdigest())
    #signature
    sig = "" + ts + "\n" + nonce + "\n" + method + "\n" + endpoint + "\n" + host + "\n" + str(port) + "\n\n"
    hmac_hex_bin = hmac.new(secret.encode('utf-8'), sig.encode('utf-8'), hashlib.sha256).digest()
    mac = base64.b64encode(hmac_hex_bin).decode()
    #authorization
    auth = 'MAC id=\"' + token + '\", nonce=\"' + nonce + '\", ts=\"' + ts + '\", mac=\"' + mac + '\"'
    return auth
####################################################################
# ================================================================
# get_key_and_iv
# ================================================================
def get_key_and_iv(
    password,
    salt,
    klen=32,
    ilen=16,
    msgdgst='md5',
    ):
    '''
    Derive the key and the IV from the given password and salt.

    This is a niftier implementation than my direct transliteration of
    the C++ code although I modified to support different digests.

    CITATION: http://stackoverflow.com/questions/13907841/implement-openssl-aes-encryption-in-python

    @param password  The password to use as the seed.
    @param salt      The salt.
    @param klen      The key length.
    @param ilen      The initialization vector length.
    @param msgdgst   The message digest algorithm to use.
    '''

    # equivalent to:
    #   from hashlib import <mdi> as mdf
    #   from hashlib import md5 as mdf
    #   from hashlib import sha512 as mdf

    mdf = getattr(__import__('hashlib', fromlist=[msgdgst]), msgdgst)
    password = password.encode('ascii', 'ignore')  # convert to ASCII

    try:
        maxlen = klen + ilen
        keyiv = mdf(password + salt).digest()
        tmp = [keyiv]
        while len(tmp) < maxlen:
            tmp.append(mdf(tmp[-1] + password + salt).digest())
            keyiv += tmp[-1]  # append the last byte
        key = keyiv[:klen]
        iv = keyiv[klen:klen + ilen]
        return (key, iv)
    except UnicodeDecodeError:
        return (None, None)
####################################################################
def encrypt_sign(data):
    data = pad(data)
    key1 = str.encode(data)
    password = \
        'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAzJ9JaHioVi6rr0TAfr6j'
    salt = os.urandom(8)
    (key, iv) = get_key_and_iv(password, salt, klen=32, ilen=16,
                               msgdgst='md5')
    #print(key)
    #print(iv)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    a = cipher.encrypt(key1)
    a = salt + a
    return base64.b64encode(a).decode()
####################################################################
def decrypt_sign(sign):
    buffer = base64.b64decode(sign)
    buffer_encoded = base64.b64encode(buffer)
    password = \
        'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAzJ9JaHioVi6rr0TAfr6j'
    salt = buffer[0:8]
    (key, iv) = get_key_and_iv(password, salt, klen=32, ilen=16,
                               msgdgst='md5')
    data = buffer[8:len(buffer)]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    a = unpad(cipher.decrypt(data)).decode('utf8')
    return json.loads(a)
