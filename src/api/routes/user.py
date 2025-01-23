from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from src.api.db import database
from src.api.repo import userrepository
from src.api.utils import schemas
from src.api.auth import oauth2

router = APIRouter(
    prefix="/user",
    tags=['Users']
)

get_db = database.get_db

@router.post('/', response_model=schemas.UserResponseModel)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    return userrepository.create(request, db)

@router.get('/{id}', response_model=schemas.UserResponseModel)
def get_user(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    user = userrepository.show(id, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found.")
    return user

@router.put('/{id}', response_model=schemas.UserResponseModel, status_code=status.HTTP_200_OK)
def update_user(id: int, request: schemas.UserUpdateModel, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return userrepository.update(id, request, db)

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    # Make sure the logged-in user is deleting their own account
    if current_user.id != id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete this user"
        )
    return userrepository.delete(id, db)
