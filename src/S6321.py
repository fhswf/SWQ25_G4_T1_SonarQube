import crypt
import secrets
from hashlib import pbkdf2_hmac

salt = secrets.token_bytes(16)
hash = pbkdf2_hmac('sha256', password, salt, 100000)    # Noncompliant: salt is hardcoded
