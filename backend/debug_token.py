from app.core.security import create_access_token, decode_token
from datetime import datetime, timezone

# Create token
token_data = {"sub": 1, "role": "admin"}
token = create_access_token(token_data)
print(f"Created token: {token[:50]}...")

# Try to decode it
try:
    decoded = decode_token(token)
    print(f"Decoded successfully: {decoded}")
except Exception as e:
    print(f"Decode failed: {e}")

# Check expiry
from jose import jwt
from app.core.config import settings
payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
print(f"Expiry: {payload.get('exp')}")
print(f"Current time: {datetime.now(timezone.utc).timestamp()}")
