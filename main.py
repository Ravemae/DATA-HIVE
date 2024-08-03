from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from sqlmodel import Session
from auth import authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from database import get_session
from routes.sign_upin import signup
from routes.users import users_routes
from routes.payments import payments_router  
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# Middleware setup for CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)

@app.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):
    user, user_type = authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "user_type": user_type},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Include routers for different routes
app.include_router(signup, tags=['Signup'])
app.include_router(users_routes, tags=['Users'])
app.include_router(payments_router, tags=['Payments'])
