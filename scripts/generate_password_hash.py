"""Create the ADMIN_PASSWORD_HASH value for your .env file.

Usage:  python scripts/generate_password_hash.py
"""

import getpass

from werkzeug.security import generate_password_hash

password = getpass.getpass("Admin password: ")
if len(password) < 12:
    raise SystemExit("Use at least 12 characters.")
if password != getpass.getpass("Repeat password: "):
    raise SystemExit("Passwords do not match.")
print("\nAdd this line to your .env file:\n")
print(f"ADMIN_PASSWORD_HASH='{generate_password_hash(password)}'")
