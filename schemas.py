from pydantic import BaseModel, Field
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Add_user(BaseModel):
    fullname: str
    email: str
    password: str
    
    def hash_password(self):
        self.password = pwd_context.hash(self.password)
        return self.password
    
class User(BaseModel):
    fullname: str
    email: str
    subscription_type: str
    subscription_status: str
    trials_used: int
    samples_used: int
    
class Admin (BaseModel):
    fullname: str
    email: str
    password: str
    profil_picpath: str
    
class filename(BaseModel):
    fullname: str
    filename_path: str
    
def hash_password(password):
    return pwd_context.hash(password)