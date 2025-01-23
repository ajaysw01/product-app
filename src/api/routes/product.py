from fastapi import APIRouter, Depends, HTTPException, status, Response
from typing import List
from src.api.db import database
from src.api.repo import productrepository
from src.api.utils import schemas
from src.api.auth import oauth2
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/products",
    tags=['Products']
)

get_db = database.get_db

@router.get('/', response_model=List[schemas.ProductResponseModel])
def get_all_products(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return productrepository.get_all(db)

@router.post('/', status_code=status.HTTP_201_CREATED)
def create_product(request: schemas.ProductCreateModel, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return productrepository.add_product(request, db)

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return productrepository.remove_product(id, db)

@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_product(id: int, request: schemas.ProductUpdateModel, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return productrepository.update_product(id, request, db)

@router.get('/{id}', status_code=200, response_model=schemas.ProductResponseModel)
def get_product(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return productrepository.get_product(id, db)
