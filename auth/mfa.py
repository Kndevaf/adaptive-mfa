import pyotp

# Generate a TOTP secret for a user (do once)
def generate_totp_secret():
    return pyotp.random_base32()

# Verify a TOTP code
def verify_totp(secret: str, token: str) -> bool:
    totp = pyotp.TOTP(secret)
    return totp.verify(token)
