from jose import JWTError, jwt
from passlib.context import CryptContext

# JWT Example
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
data = {"sub": "test"}

token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
print(f"Encoded JWT: {token}")

try:
    decoded_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    print(f"Decoded JWT: {decoded_data}")
except JWTError as e:
    print(f"JWT error: {e}")

# Passlib Example
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
password = "mysecretpassword"
hashed_password = pwd_context.hash(password)
print(f"Hashed password: {hashed_password}")

is_verified = pwd_context.verify(password, hashed_password)
print(f"Password verified: {is_verified}")
