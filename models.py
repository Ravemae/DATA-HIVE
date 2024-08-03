from sqlmodel import Field, SQLModel
from database import create_db_and_tables

class User(SQLModel, table=True):
    __tablename__ = 'Users_db'
    
    id: int = Field(primary_key=True)
    fullname: str = Field(unique=True)
    email: str = Field(unique=True)
    password: str
    profil_pic: str = Field(default=None)
    subscription_type: str = Field(default="Free")
    subscription_status: str = Field(default="Inactive")
    trials_used: int = Field(default=0)
    samples_used: int = Field(default=0)
    
class Admin(SQLModel, table=True):
    id: int = Field(primary_key=True)
    fullname: str = Field(unique=True)
    email: str = Field(unique=True)
    password: str
    
class File(SQLModel, table=True):
    id :int = Field(primary_key=True)
    filename: str
    file_path: str
    fullname: str
    
create_db_and_tables()
