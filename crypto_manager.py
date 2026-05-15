import base64
import os
from datetime import datetime

from Crypto.Cipher import ChaCha20, AES
from Crypto.Util.Padding import pad, unpad

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

from config import PROTECTED_COLUMNS, HASH_COLUMNS, CERT_FILES
from hasher import update_row_hash, verify_row_hash


def load_public_key_from_certificate():
    with open(CERT_FILES["client_cert"], "rb") as cert_file:
        cert_data = cert_file.read()
    certificate = x509.load_pem_x509_certificate(cert_data)
    return certificate.public_key()


def load_private_key():
    with open(CERT_FILES["client_private_key"], "rb") as key_file:
        key_data = key_file.read()
    return serialization.load_pem_private_key(key_data, password=None)


def wrap_key_with_certificate(sym_key):
    public_key = load_public_key_from_certificate()
    encrypted_key = public_key.encrypt(
        sym_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return base64.b64encode(encrypted_key).decode("utf-8")


def unwrap_key_with_private_key(encrypted_key_b64):
    private_key = load_private_key()
    encrypted_key = base64.b64decode(encrypted_key_b64.encode("utf-8"))
    sym_key = private_key.decrypt(
        encrypted_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return sym_key


def encrypt_chacha20(value, key, nonce):
    cipher = ChaCha20.new(key=key, nonce=nonce)
    ciphertext = cipher.encrypt(str(value).encode("utf-8"))
    return base64.b64encode(ciphertext).decode("utf-8")


def decrypt_chacha20(value, key, nonce):
    cipher = ChaCha20.new(key=key, nonce=nonce)
    plaintext = cipher.decrypt(base64.b64decode(value.encode("utf-8")))
    return plaintext.decode("utf-8")


def encrypt_aes(value, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(str(value).encode("utf-8"), AES.block_size))
    return base64.b64encode(ciphertext).decode("utf-8")


def decrypt_aes(value, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(base64.b64decode(value.encode("utf-8"))), AES.block_size)
    return plaintext.decode("utf-8")


def encrypt_row(row, dataset_name):
    if str(row.get("enc_status", "plaintext")).lower() == "encrypted":
        return row

    columns = PROTECTED_COLUMNS[dataset_name]

    if dataset_name == "PMD":
        sym_key = os.urandom(32)
        nonce = os.urandom(12)

        for col in columns:
            row[col] = encrypt_chacha20(row[col], sym_key, nonce)

        row["enc_algorithm"] = "ChaCha20+RSA"
        row["nonce_or_iv"] = base64.b64encode(nonce).decode("utf-8")
        row["encrypted_key"] = wrap_key_with_certificate(sym_key)

    else:
        sym_key = os.urandom(16)
        iv = os.urandom(16)

        for col in columns:
            row[col] = encrypt_aes(row[col], sym_key, iv)

        row["enc_algorithm"] = "AES-CBC+RSA"
        row["nonce_or_iv"] = base64.b64encode(iv).decode("utf-8")
        row["encrypted_key"] = wrap_key_with_certificate(sym_key)

    row["enc_status"] = "encrypted"
    row["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row = update_row_hash(row, HASH_COLUMNS[dataset_name])
    return row


def decrypt_row(row, dataset_name):
    if str(row.get("enc_status", "plaintext")).lower() != "encrypted":
        return row

    if not verify_row_hash(row, HASH_COLUMNS[dataset_name]):
        raise ValueError("Integrity check failed. Row may have been tampered with.")

    columns = PROTECTED_COLUMNS[dataset_name]
    nonce_or_iv = base64.b64decode(row["nonce_or_iv"])
    sym_key = unwrap_key_with_private_key(row["encrypted_key"])

    if dataset_name == "PMD":
        for col in columns:
            row[col] = decrypt_chacha20(row[col], sym_key, nonce_or_iv)
    else:
        for col in columns:
            row[col] = decrypt_aes(row[col], sym_key, nonce_or_iv)

    row["enc_status"] = "plaintext"
    row["enc_algorithm"] = "none"
    row["nonce_or_iv"] = "none"
    row["encrypted_key"] = "none"
    row["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row = update_row_hash(row, HASH_COLUMNS[dataset_name])
    return row


def preview_decrypt_row(row, dataset_name):
    temp_row = row.copy()

    if str(temp_row.get("enc_status", "plaintext")).lower() != "encrypted":
        return temp_row, "plaintext"

    if not verify_row_hash(temp_row, HASH_COLUMNS[dataset_name]):
        raise ValueError("Integrity check failed. Encrypted row may have been tampered with.")

    columns = PROTECTED_COLUMNS[dataset_name]
    nonce_or_iv = base64.b64decode(temp_row["nonce_or_iv"])
    sym_key = unwrap_key_with_private_key(temp_row["encrypted_key"])

    if dataset_name == "PMD":
        for col in columns:
            temp_row[col] = decrypt_chacha20(temp_row[col], sym_key, nonce_or_iv)
    else:
        for col in columns:
            temp_row[col] = decrypt_aes(temp_row[col], sym_key, nonce_or_iv)

    return temp_row, "preview_decrypted"