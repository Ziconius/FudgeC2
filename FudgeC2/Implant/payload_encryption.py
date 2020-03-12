from Crypto.Cipher import AES
import json
from base64 import b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

from base64 import b64encode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes

class PayloadEncryption():
    # TODO: The remaining client-side code should be bundled in here before finalising the 0.5.6 release

    @staticmethod
    def encrypt_with_static_aes(payload):
        # Responsible for encrypting the secondary payload using a static key.
        # Returns a dict with IV, Ciphertext and Key, all as base64 values.
        # These can then be inserted into the client-side decryption routine.
        key = get_random_bytes(16)
        cipher = AES.new(key, AES.MODE_CBC)
        ct_bytes = cipher.encrypt(pad(payload.encode(), AES.block_size))
        iv = b64encode(cipher.iv).decode('utf-8')
        ct = b64encode(ct_bytes).decode('utf-8')
        key = b64encode(key).decode('utf-8')
        result = {'key': key, 'iv': iv, 'ciphertext': ct}
        return result