import hashlib
import hmac

from argon2 import PasswordHasher
from cryptography.fernet import Fernet

from app.core.config import settings


password_hasher = PasswordHasher()

fernet = Fernet(settings.mobile_encryption_key.encode())


def hash_password(password: str) -> str:
    """Create a secure Argon2id password hash."""
    return password_hasher.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    """Verify a plaintext password against an Argon2id hash."""
    try:
        return password_hasher.verify(password_hash, password)
    except Exception:
        return False


def encrypt_mobile(mobile: str) -> str:
    """Encrypt a mobile number for secure storage."""
    return fernet.encrypt(mobile.encode()).decode()


def decrypt_mobile(encrypted_mobile: str) -> str:
    """Decrypt a stored mobile number."""
    return fernet.decrypt(encrypted_mobile.encode()).decode()


def hash_mobile(mobile: str) -> str:
    """
    Create a deterministic HMAC-SHA256 hash for exact-match lookup.

    HMAC is used instead of plain SHA-256 so that an attacker
    cannot cheaply precompute hashes of possible phone numbers.
    """
    normalized = normalize_mobile(mobile)

    return hmac.new(
        settings.mobile_hash_secret.encode(),
        normalized.encode(),
        hashlib.sha256,
    ).hexdigest()


def normalize_mobile(mobile: str) -> str:
    """Normalize mobile numbers before encryption/hash lookup."""
    return "".join(char for char in mobile if char.isdigit())