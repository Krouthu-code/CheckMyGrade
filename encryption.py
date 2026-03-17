"""
encryption.py
Simple password encryption and decryption using base64.
This is beginner-friendly — NOT for real-world use.
"""

import base64


def encrypt_password(password):
    """Encrypt a password using base64 encoding."""
    encoded = base64.b64encode(password.encode("utf-8"))
    return encoded.decode("utf-8")


def decrypt_password(encrypted):
    """Decrypt a base64-encoded password back to plain text."""
    decoded = base64.b64decode(encrypted.encode("utf-8"))
    return decoded.decode("utf-8")
