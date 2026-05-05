from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from typing import Optional
from config.settings import get_settings


settings = get_settings()

pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto",

    # Argon2 tuning parameters — adjust based on your server capacity
    # OWASP recommended minimums:
    argon2__memory_cost=65536,   # 64 MB memory usage per hash
    argon2__time_cost=3,         # number of iterations
    argon2__parallelism=2,       # parallel threads
    argon2__hash_len=32,         # output hash length in bytes
    argon2__salt_size=16,        # random salt size in bytes — auto-generated
    argon2__type="ID",           # argon2id — best variant (resists side-channel + GPU)
)

def hash_password(plain_password: str) -> str:
    """
    Hashes plain text using Argon2id with auto-generated random salt.
    Produces a self-contained hash string like:
    $argon2id$v=19$m=65536,t=3,p=2$<salt>$<hash>
    Salt is embedded — no separate column needed.
    """
    return pwd_context.hash(plain_password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies plain password against stored Argon2 hash.
    Passlib extracts salt + params from the hash string automatically.
    """
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def decode_token(token: str) -> dict:
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])