# from sqlmodel import Field, SQLModel , Session
# from database import create_db_and_tables

# class User(SQLModel, table=True):
#     __tablename__ = 'Users_db'

#     id: int = Field(primary_key=True)
#     fullname: str = Field(unique=True)
#     email: str = Field(unique=True)
#     password: str
#     profil_pic: str = Field(default=None)

# class Admin(SQLModel, table=True):
#     id: int = Field(primary_key=True)
#     fullname: str = Field(unique=True)
#     email: str = Field(unique=True)
#     password: str

# class files(SQLModel, table= True):
#     id: int = Field(primary_key=True)
#     filename: str
#     file_path: str
#     fullname: str


# create_db_and_tables()