users = {
    "admin": {
        "password": hash_password("Password123"),
        "mfa_enabled": True,
        "totp_secret": "JBSWY3DPEHPK3PXP"  # Example secret, generate dynamically in production
    },
    "user": {
        "password": hash_password("UserPass456"),
        "mfa_enabled": False,
        "totp_secret": None
    }
}
