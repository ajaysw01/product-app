from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends
from src.api.db import models
from src.api.utils import schemas
from src.api.auth import oauth2


def get_all(db: Session):
    products = db.query(models.Product).all()
    return products


def add_product(request: schemas.ProductBaseModel, db: Session, current_user: models.User):
    new_product = models.Product(
        name=request.name,
        description=request.description,
        price=request.price,
        user_id=current_user.id,
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


def remove_product(id: int, db: Session):
    product = db.query(models.Product).filter(models.Product.id == id).first()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {id} not found"
        )

    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully"}

def update_product(id: int, request: schemas.ProductUpdateModel, db: Session):
    product = db.query(models.Product).filter(models.Product.id == id).first()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {id} not found"
        )

    if request.name:
        product.name = request.name
    if request.description:
        product.description = request.description
    if request.price:
        product.price = request.price

    db.commit()
    db.refresh(product)
    return product

def get_product(id: int, db: Session):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {id} not found"
        )
    return product
