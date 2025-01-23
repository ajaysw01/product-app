from fastapi import APIRouter, Depends, status,HTTPException
from sqlalchemy.orm import Session
from src.api.db import  database
from src.api.repo import userrepository
from src.api.utils import schemas

router = APIRouter(
    prefix="/user",
    tags=['Users']
)

get_db = database.get_db


@router.post('/', response_model=schemas.ShowUser)
def create_user(request: schemas.User,db: Session = Depends(get_db)):
    return userrepository.create(request,db)

@router.get('/{id}', response_model=schemas.ShowUser)
def get_user(id: int, db: Session = Depends(get_db)):
    user = userrepository.show(id, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found.")
    return user
