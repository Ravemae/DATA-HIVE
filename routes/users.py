from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from fastapi.responses import FileResponse
from sqlmodel import Session, select
from auth import get_current_active_user
from database import get_session
from model import User, files
import mimetypes
import os
import shutil
from visualization import visualize_data
from ai import insights

users_route = APIRouter()

@users_route.get("/user/details")
async def get_user_details(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    user = session.exec(select(User).where(User.id == current_user["user"].id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "full_name": user.fullname,
        "email": user.email,
    }

UPLOAD_DIRECTORY = './uploads'
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

@users_route.post("/user/uploadfile")
async def upload_file(file: UploadFile = File(...),
                      session: Session = Depends(get_session),
                      current_user: User = Depends(get_current_active_user)):
    # Check file type
    mimetype, _ = mimetypes.guess_type(file.filename)
    if mimetype not in ["text/csv", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "application/vnd.ms-excel"]:
        raise HTTPException(status_code=400, detail="Only CSV or Excel files are allowed.")
    
    file_path = f"uploads/{file.filename}"
    
    # Ensure the uploads directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    # Save the file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    user = session.exec(select(User).where(User.id == current_user['user'].id)).first()
    
    new_file = files(
        file_path=file_path,
        fullname=user.fullname,
        filename=file.filename,
    )

    session.add(new_file)
    session.commit()
    session.refresh(new_file)

    return {"message": "File added successfully.", "filename": file.filename}



@users_route.get("/user/getfiles")
async def get_all_files(session: Session = Depends(get_session), 
                      current_user: User = Depends(get_current_active_user)):
    fls = session.exec(select(files).where(files.fullname == current_user['user'].fullname)).all()
    binder =[]
    for file in fls:
      binder.append({"filename": file.filename})
    return binder
    # return binder


@users_route.get("/user/getfile/{filename}")
async def get_single_file(
    filename: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    file = session.exec(select(files).where(
        files.filename == filename,
        files.fullname == current_user['user'].fullname
    )).first()
    if file is None:
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path=file.file_path, filename=file.filename) 



@users_route.get('/user/visuals/analysis/{filename}')
async def visualize(filename: str,
                    session: Session = Depends(get_session),
                    current_user: User = Depends(get_current_active_user)):
    file = session.exec(select(files).where(
        files.filename == filename,
        files.fullname == current_user['user'].fullname
    )).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    results = {'visuals': visualize_data(file.file_path, current_user['user'].fullname), 'insights': insights(file.file_path)}
    return results