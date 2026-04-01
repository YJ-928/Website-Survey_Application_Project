import logging
from functools import lru_cache
from django.conf import settings
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

logger = logging.getLogger(__name__)


@lru_cache
def read_public_key():
    try:
        key_path = settings.ENCRYPTION_PUBLIC_KEY_PATH
    except AttributeError:
        raise ValueError("ENCRYPTION_PUBLIC_KEY_PATH not configured in settings")

    try:
        with open(key_path, "rb") as key_file:
            public_key = serialization.load_pem_public_key(
                key_file.read()
            )
            return public_key

    except FileNotFoundError:
        logger.error("Public key file not found at configured path")
        raise
    except Exception:
        logger.exception("Failed to load public key")
        raise


def encrypt_to_hex(message: str) -> str:
    if not message:
        raise ValueError("Message cannot be empty")

    try:
        public_key = read_public_key()
        encrypted_bytes = public_key.encrypt(
            message.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
        return encrypted_bytes.hex()

    except Exception:
        logger.exception("Encryption failed")
        raise ValueError("Failed to encrypt message")
