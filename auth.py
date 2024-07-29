import logging
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from sqlmodel import Session, select
from database import get_session
from models import Admin, User

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SECRET_KEY = "b0423fa3267456528ac05011df658b4e7d0063f6f79a30120b1d3a009f0cc65d"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(email: str, password: str, session: Session):
    logger.info(f"Authenticating user with email: {email}")
    user = session.exec(select(Admin).where(Admin.email == email)).first()
    if user and verify_password(password, user.password):
        logger.info("Admin authenticated successfully")
        return user, "admin"
    
    user = session.exec(select(User).where(User.email == email)).first()
    if user and verify_password(password, user.password):
        logger.info("User authenticated successfully")
        return user, "client"
    
    logger.warning("Authentication failed")
    return None, None

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = session.exec(select(Admin).where(Admin.email == email)).first()
    user_type = "admin" if user else None

    if not user:
        user = session.exec(select(User).where(User.email == email)).first()
        user_type = "client" if user else None

    if user is None:
        raise credentials_exception

    return {"user": user, "user_type": user_type}

def get_current_active_user(current_user: dict = Depends(get_current_user)):
    if not current_user["user"]:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def get_current_active_admin(current_user: dict = Depends(get_current_active_user)):
    if current_user["user_type"] != "admin":
        raise HTTPException(status_code=403, detail="Not Authorized")
    return current_user["user"]

def get_current_active_client(current_user: dict = Depends(get_current_active_user)):
    if current_user["user_type"] != "client":
        raise HTTPException(status_code=403, detail="Not Authorized")
    return current_user["user"]


