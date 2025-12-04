from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
import base64

def load_public_key(path="instructor_public.pem"):
    with open(path, "rb") as f:
        return serialization.load_pem_public_key(f.read())

if __name__ == "__main__":
    # Load signature
    with open("signature.bin", "rb") as f:
        sig = f.read()

    # Load instructor public key
    pub = load_public_key()

    encrypted = pub.encrypt(
        sig,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    encoded = base64.b64encode(encrypted).decode("utf-8")

    with open("encrypted_signature.txt", "w") as f:
        f.write(encoded)

    print("✔ encrypted_signature.txt created!")
    print("\n--- COPY THIS FOR SUBMISSION ---\n")
    print(encoded)
