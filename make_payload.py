import json

with open("student_public.pem", "r") as f:
    pubkey = f.read()

payload = {
    "student_id": "23A91A05E5",
    "github_repo_url": "https://github.com/prasannnna/GPP-task-2",
    "public_key": pubkey
}

with open("payload.json", "w") as f:
    json.dump(payload, f, indent=2)

print("✅ payload.json created!")
