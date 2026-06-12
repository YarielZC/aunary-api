# src/modules/dev/router.py
import time
import uuid
import json
import base64
import hashlib
from fastapi import APIRouter
from pydantic import BaseModel
import jwt
from cryptography.hazmat.primitives.asymmetric import rsa
from jwt.algorithms import RSAAlgorithm

router = APIRouter(prefix="/dev", tags=["Development Only"])

private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
jwk_dict = json.loads(RSAAlgorithm.to_jwk(private_key.public_key()))
jwk_dict["alg"] = "RS256"

class DpopRequest(BaseModel):
    method: str
    url: str
    access_token: str | None = None

@router.post("/generate-dpop")
async def dev_generate_dpop(req: DpopRequest):
    """Genera un Proof DPoP para ser consumido por la extensión REST Client"""
    headers = {"typ": "dpop+jwt", "alg": "RS256", "jwk": jwk_dict}
    payload = {
        "jti": str(uuid.uuid4()),
        "htm": req.method,
        "htu": req.url,
        "iat": int(time.time())
    }
    
    if req.access_token:
        ath = base64.urlsafe_b64encode(
            hashlib.sha256(req.access_token.encode("utf-8")).digest()
        ).decode().rstrip("=")
        payload["ath"] = ath
        
    proof = jwt.encode(payload, private_key, algorithm="RS256", headers=headers)
    return {"proof": proof}