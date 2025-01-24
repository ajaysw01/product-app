from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from src.api.db import database, models
from src.api.repo import productrepository
from src.api.utils import schemas
from src.api.auth import oauth2
from sqlalchemy.orm import Session
import datetime
import csv
import os
import json

# Define the folder where exported files will be stored
EXPORT_FOLDER = "exports"
os.makedirs(EXPORT_FOLDER, exist_ok=True)

router = APIRouter(prefix="/products", tags=["Products"])

get_db = database.get_db

@router.get("/", response_model=List[schemas.ProductResponseModel])
def get_all_products(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return productrepository.get_all(db)

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_product(
    request: schemas.ProductBaseModel,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    return productrepository.add_product(request, db, current_user)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    id: int, 
    db: Session = Depends(get_db), 
    current_user: schemas.User = Depends(oauth2.get_current_user),
):
    return productrepository.remove_product(id, db)

@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_product(
    id: int,
    request: schemas.ProductUpdateModel,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):
    return productrepository.update_product(id, request, db)

@router.get("/export", status_code=status.HTTP_200_OK)
def export_products_to_file(
    format: str = "csv",  # Default format is CSV
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    products = db.query(models.Product).filter(models.Product.user_id == current_user.id).all()

    if not products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No products found for the current user.",
        )

    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    if format == "csv":
        file_path = _export_to_csv(products, timestamp)
    elif format == "json":
        file_path = _export_to_json(products, timestamp)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid format. Supported formats are 'csv' and 'json'.",
        )

    return {"message": f"Products exported successfully to {file_path}"}

def _export_to_csv(products, timestamp):
    file_path = os.path.join(EXPORT_FOLDER, f"products_{timestamp}.csv")
    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Name", "Description", "Price", "User ID"])
        for product in products:
            writer.writerow([product.id, product.name, product.description, product.price, product.user_id])
    return file_path

def _export_to_json(products, timestamp):
    file_path = os.path.join(EXPORT_FOLDER, f"products_{timestamp}.json")
    with open(file_path, mode="w", encoding="utf-8") as file:
        product_list = [
            {
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "price": product.price,
                "user_id": product.user_id,
            }
            for product in products
        ]
        json.dump(product_list, file, indent=4)
    return file_path

@router.get("/{id}", status_code=200, response_model=schemas.ProductResponseModel)
def get_product(
    id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):
    return productrepository.get_product(id, db)
