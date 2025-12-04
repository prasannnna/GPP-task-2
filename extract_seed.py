import json

with open("seed_response.json", "r") as f:
    data = json.load(f)

seed = data.get("encrypted_seed")
if not seed:
    print("❌ encrypted_seed not found!")
    exit()

with open("encrypted_seed.txt", "w") as f:
    f.write(seed)

print("✅ encrypted_seed.txt saved (DO NOT commit this file)")
