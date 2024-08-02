from fastapi import APIRouter, Depends
from models import User
from schemas  import Add_user, hash_password
from sqlmodel import Session
from database import get_session

signup =  APIRouter()


@signup.post("/user/signup", response_model= User )
def create_user(userdata: Add_user, session: Session= Depends(get_session)) :
    userdata.password = hash_password(userdata.password)
    user =  User(
        fullname= userdata.fullname,
        email= userdata.email,
        password= userdata.password,

    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
    
    

