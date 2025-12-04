# app/crypto_utils.py
import base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

def load_private_key(path: str):
    with open(path, "rb") as f:
        return serialization.load_pem_private_key(f.read(), password=None)

def decrypt_seed(encrypted_seed_b64: str, private_key) -> str:
    """
    Decrypt base64-encoded encrypted seed using RSA/OAEP(SHA-256)
    """
    # 1. base64 → bytes
    ciphertext = base64.b64decode(encrypted_seed_b64)

    # 2. RSA/OAEP decrypt
    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # 3. decode plaintext to UTF-8 hex seed
    hex_seed = plaintext.decode("utf-8").strip()

    # 4. validate seed
    if len(hex_seed) != 64 or any(c not in "0123456789abcdef" for c in hex_seed.lower()):
        raise ValueError("Invalid decrypted seed")

    return hex_seed.lower()
