# AES-CBC block cipher for structured patient records
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

# Sample combined healthcare record
record_data = b"PAD: Admin-WardA | PFD: Bill-PKR45000"

# Secret key generation
block_key = get_random_bytes(16)

# Encryption
block_cipher = AES.new(block_key, AES.MODE_CBC)
encrypted_record = block_cipher.encrypt(pad(record_data, AES.block_size))
print("Encrypted Record:", encrypted_record)

# Decryption
block_decipher = AES.new(block_key, AES.MODE_CBC, iv=block_cipher.iv)
decrypted_record = unpad(block_decipher.decrypt(encrypted_record), AES.block_size)
print("Decrypted Record:", decrypted_record.decode())