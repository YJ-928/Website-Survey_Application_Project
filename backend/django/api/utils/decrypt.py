import logging
from functools import lru_cache

from django.conf import settings
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

logger = logging.getLogger(__name__)


@lru_cache
def read_private_key():
    """
    Read and load the private RSA key from file.
    Cached to avoid repeated disk reads.
    """
    try:
        key_path = settings.ENCRYPTION_PRIVATE_KEY_PATH
    except AttributeError:
        raise ValueError(
            "ENCRYPTION_PRIVATE_KEY_PATH not configured in settings"
        )

    try:
        with open(key_path, "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None,
            )
            return private_key

    except FileNotFoundError:
        logger.error(
            "Private key file not found at configured path: %s",
            key_path,
        )
        raise
    except Exception:
        logger.exception("Failed to load private RSA key")
        raise


def decrypt_password(encrypted_password: str) -> str:
    """
    Decrypt RSA-encrypted password (hex string).

    Raises:
        ValueError: If input is invalid or decryption fails
    """

    # Guard: empty or plain text (very short strings)
    if not encrypted_password or len(encrypted_password) < 32:
        raise ValueError("Password must be RSA encrypted")

    # Convert hex to bytes
    try:
        encrypted_bytes = bytes.fromhex(encrypted_password)
    except ValueError:
        raise ValueError("Invalid encrypted password format")

    try:
        private_key = read_private_key()

        decrypted_bytes = private_key.decrypt(
            encrypted_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )

        return decrypted_bytes.decode()

    except ValueError:
        logger.warning(
            "Password decryption failed (invalid ciphertext)"
        )
        raise ValueError("Invalid encrypted password")

    except Exception:
        logger.exception("Unexpected error during password decryption")
        raise ValueError("Password decryption failed")
