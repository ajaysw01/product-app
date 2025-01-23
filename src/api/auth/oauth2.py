from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from src.api.db import models, database
from src.api.auth import jwt_token 
get_db = database.get_db
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    email = jwt_token.verify_token(token, credentials_exception)  
    
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise credentials_exception
    
    return user
