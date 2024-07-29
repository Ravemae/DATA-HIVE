# from pydantic import BaseModel, Field
# from passlib.context import CryptContext

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# class Add_user(BaseModel):
#     fullname: str 
#     email: str 
#     password: str
#     profil_picpath: str
#     def hash_password(self):
#         self.password = pwd_context.hash(self.password)
#         return self.password 



# class Admin(BaseModel):
#     fullname: str 
#     email: str 
#     password: str
#     profil_picpath: str


# class Filename(BaseModel):
#     fullname: str
#     filename_path: str


# def hash_password(password):
#         return pwd_context.hash(password)