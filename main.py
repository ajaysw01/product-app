from fastapi import FastAPI
from src.api.db import  models
from src.api.db import database
from  src.api.routes import product, user
from src.api.auth import authentication

app = FastAPI()

models.Base.metadata.create_all(database.engine)

app.include_router(product.router)
app.include_router(user.router)
app.include_router(authentication.router)

@app.get("/")
async def health_check():
    return {"message" :"App is working fine"}

