from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from fastapi.responses import FileResponse
from fastapi import Body
from typing import List
from sqlmodel import Session, select
from auth import get_current_active_user
from database import get_session
from models import User, File as FileModel
import mimetypes
import os
import shutil
from visualization import visualize_data
from ai import insights
from utils.files import convert_to_pdf, custom_analysis, clean_data

users_routes = APIRouter()

SUBSCRIPTION_LIMITS = {
    "Free": {"samples": 5, "trials": 10},
    "Pro": {"samples": 10, "trials": 20},
    "Premium": {"samples": float('inf'), "trials": float('inf')}
}

@users_routes.get("/user/details")
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
        "subscription_type": user.subscription_type,
        "subscription_status": user.subscription_status,
        "trials_used": user.trials_used,
        "samples_used": user.samples_used,
    }
    
    
UPLOAD_DIRECTORY = './uploads'
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

@users_routes.post("/user/uploadfile")
async def upload_file(file: UploadFile = File(...),
                      session: Session = Depends(get_session),
                      current_user: User = Depends(get_current_active_user)):
    user = session.exec(select(User).where(User.id == current_user['user'].id)).first()
    

    mimetype, _ = mimetypes.guess_type(file.filename)
    if mimetype not in ["text/csv", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "application/vnd.ms-excel"]:
        raise HTTPException(status_code=400, detail="Only CSV or Excel files are allowed.")
    
    limits = SUBSCRIPTION_LIMITS[user.subscription_type]
    if user.samples_used >= limits["samples"]:
        raise HTTPException(status_code=403, detail="Sample limit reached for your subscription plan.")
    
    file_path = f"uploads/{file.filename}"
    
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    # Save the file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    new_file = FileModel(
        file_path=file_path,
        fullname=user.fullname,
        filename=file.filename,
    )

    session.add(new_file)
    session.commit()
    session.refresh(new_file)

    user.samples_used += 1
    session.commit()

    return {"message": "File added successfully.", "filename": file.filename}

@users_routes.get("/user/getfiles")
async def get_all_files(session: Session = Depends(get_session), 
                        current_user: User = Depends(get_current_active_user)):
    fls = session.exec(select(FileModel).where(FileModel.fullname == current_user['user'].fullname)).all()
    binder = []
    for file in fls:
        binder.append({"filename": file.filename})
    return binder

@users_routes.get("/user/getfile/{filename}")
async def get_single_file(
    filename: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    file = session.exec(select(FileModel).where(
        FileModel.filename == filename,
        FileModel.fullname == current_user['user'].fullname
    )).first()
    if file is None:
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path=file.file_path, filename=file.filename)

@users_routes.get('/user/visuals/analysis/{filename}')
async def visualize(filename: str,
                    session: Session = Depends(get_session),
                    current_user: User = Depends(get_current_active_user)):
    user = session.exec(select(User).where(User.id == current_user['user'].id)).first()
    
    limits = SUBSCRIPTION_LIMITS[user.subscription_type]
    if user.trials_used >= limits["trials"]:
        raise HTTPException(status_code=403, detail="Trial limit reached for your subscription plan.")
    
    file = session.exec(select(FileModel).where(
        FileModel.filename == filename,
        FileModel.fullname == current_user['user'].fullname
    )).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    
    results = {'visuals': visualize_data(file.file_path, current_user['user'].fullname), 'insights': insights(file.file_path)}

    # Increment the trials used counter
    user.trials_used += 1
    session.commit()
    
    return results

@users_routes.post("/user/convert_to_pdf")
async def convert_file_to_pdf(
    file: UploadFile = File(...),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    user = session.exec(select(User).where(User.id == current_user['user'].id)).first()
    
    file_extension = os.path.splitext(file.filename)[1]
    if file_extension not in [".csv", ".xls", ".xlsx"]:
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    output_file = f"{os.path.splitext(file.filename)[0]}.pdf"
    input_file_path = f"uploads/{file.filename}"
    output_file_path = f"uploads/{output_file}"
    
    with open(input_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    convert_to_pdf(input_file_path, output_file_path)
    
    return FileResponse(output_file_path, filename=output_file)

@users_routes.post("/user/custom_analysis")
async def perform_custom_analysis(
    file: UploadFile = File(...),
    columns: List[str] = Body(...),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    user = session.exec(select(User).where(User.id == current_user['user'].id)).first()
    
    file_extension = os.path.splitext(file.filename)[1]
    if file_extension not in [".csv", ".xls", ".xlsx"]:
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    input_file_path = f"uploads/{file.filename}"
    
    with open(input_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    analysis_result = custom_analysis(input_file_path, columns)
    
    # Convert analysis result to PDF
    output_file_path = f"uploads/{os.path.splitext(file.filename)[0]}_analysis.pdf"
    convert_to_pdf(analysis_result, output_file_path)
    
    return FileResponse(output_file_path, filename=f"{os.path.splitext(file.filename)[0]}_analysis.pdf")

@users_routes.post("/user/clean_data")
async def clean_dataset(
    file: UploadFile = File(...),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    user = session.exec(select(User).where(User.id == current_user['user'].id)).first()
    
    file_extension = os.path.splitext(file.filename)[1]
    if file_extension not in [".csv", ".xls", ".xlsx"]:
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    input_file_path = f"uploads/{file.filename}"
    output_file_path = f"uploads/cleaned_{file.filename}"
    
    with open(input_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    clean_data(input_file_path, output_file_path)
    
    return {"message": "Data cleaned successfully.", "output_file": output_file_path}
