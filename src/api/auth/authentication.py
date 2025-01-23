from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from src.api.db import  database
from src.api.db import models
from src.api.utils import hashing
from src.api.auth import  token

router = APIRouter(
    tags=["Authentication"]
)

@router.post("/login")
def login(request:OAuth2PasswordRequestForm= Depends(), db: Session = Depends(database.get_db)):
    # Find user by email
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid credentials"
        )
    
    if not hashing.Hash.verify(request.password,user.password) :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid credentials"
        )

    # generate jwt token and return it
    # access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = token.create_access_token(
        data = {"sub":user.email}
    )
    return {"access_token":access_token, "token_type":"bearer"}