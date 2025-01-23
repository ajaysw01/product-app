from sqlalchemy.orm import Session
from fastapi import HTTPException, status,Depends
from src.api.utils import schemas, hashing
from src.api.auth import oauth2
from src.api.db import models

def create(request: schemas.User, db: Session):
    existing_user = db.query(models.User).filter(models.User.email == request.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered.")
    
    new_user = models.User(
        name=request.name,
        email=request.email,
        password=hashing.Hash.bcrypt(request.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def show(id: int, db: Session):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the id {id} is not available")
    return user

def delete(id: int, db: Session, current_user: schemas.User):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id {id} not found"
        )
    
    # Check if the logged-in user is the one performing the deletion
    if current_user.id != id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete this user"
        )

    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}

def update(id: int, request: schemas.UserUpdateModel, db: Session, current_user: schemas.User):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} not found"
        )
    
    # Check if the logged-in user is the one performing the update
    if current_user.id != id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to update this user"
        )

    if request.name:
        user.name = request.name

    db.commit()
    db.refresh(user)
    return user
