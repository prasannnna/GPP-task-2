# app/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pathlib import Path
import time, os

from app.crypto_utils import load_private_key, decrypt_seed
from app.totp_utils import generate_totp_code, verify_totp_code

app = FastAPI()
DATA_DIR = Path("/data") 
 
SEED_FILE = DATA_DIR / "seed.txt"

PRIVATE_KEY_PATH = Path("student_private.pem")

class DecryptPayload(BaseModel):
    encrypted_seed: str

class VerifyPayload(BaseModel):
    code: str

@app.post("/decrypt-seed")
def decrypt_seed_api(payload: DecryptPayload):
    try:
        private_key = load_private_key(str(PRIVATE_KEY_PATH))
        hex_seed = decrypt_seed(payload.encrypted_seed, private_key)
    except Exception:
        raise HTTPException(status_code=500, detail={"error": "Decryption failed"})

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    SEED_FILE.write_text(hex_seed)
    return {"status": "ok"}

@app.get("/generate-2fa")
def generate_2fa():
    if not SEED_FILE.exists():
        raise HTTPException(status_code=500, detail={"error": "Seed not decrypted yet"})

    hex_seed = SEED_FILE.read_text().strip()
    code = generate_totp_code(hex_seed)
    valid_for = 30 - (int(time.time()) % 30)

    return {"code": code, "valid_for": valid_for}

@app.post("/verify-2fa")
def verify_2fa(payload: VerifyPayload):
    if not payload.code:
        raise HTTPException(status_code=400, detail={"error": "Missing code"})

    if not SEED_FILE.exists():
        raise HTTPException(status_code=500, detail={"error": "Seed not decrypted yet"})

    hex_seed = SEED_FILE.read_text().strip()
    valid = verify_totp_code(hex_seed, payload.code, valid_window=1)

    return {"valid": valid}

@app.get("/health")
def health():
    return {"status": "ok"}
