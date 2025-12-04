from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

def load_private_key(path="student_private.pem"):
    with open(path, "rb") as f:
        return serialization.load_pem_private_key(f.read(), password=None)

def sign_message(message: str, private_key):
    # SIGN ASCII STRING EXACTLY
    return private_key.sign(
        message.encode("utf-8"),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

if __name__ == "__main__":
    commit_hash = "cd8e0910441a512d6a2dd70a277a6019cb677bff"
    key = load_private_key()
    sig = sign_message(commit_hash, key)

    with open("signature.bin", "wb") as f:
        f.write(sig)

    print("✔ signature.bin created!")
