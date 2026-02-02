from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
MAX_PASSWORD_BYTES = 72

def get_password_hash(password: str) -> str:
    password_bytes = password.encode("utf-8")
    if len(password_bytes) > MAX_PASSWORD_BYTES:
        password_bytes = password_bytes[:MAX_PASSWORD_BYTES]
    return pwd_context.hash(password_bytes.decode("utf-8"))

def verify_password(plain_password: str, hashed_password: str) -> bool:
    password_bytes = plain_password.encode("utf-8")
    if len(password_bytes) > MAX_PASSWORD_BYTES:
        password_bytes = password_bytes[:MAX_PASSWORD_BYTES]
    return pwd_context.verify(password_bytes.decode("utf-8"), hashed_password)
