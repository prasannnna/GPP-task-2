# PKI-Based 2FA Service

Simple microservice implementing:
- RSA/OAEP decryption (SHA-256)
- TOTP generation (SHA-1, 6 digits, 30s)
- TOTP verification with ±1 window
- Cron job logging codes every minute
- Docker container with FastAPI + cron

## Endpoints
POST /decrypt-seed  
GET /generate-2fa  
POST /verify-2fa

## Run with Docker
docker compose build  
docker compose up -d

## Cron Output
docker exec pki-2fa-app cat /cron/last_code.txt
