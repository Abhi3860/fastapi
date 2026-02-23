from fastapi import FastAPI
from .database import engine, get_db
from sqlmodel import SQLModel
from sqlmodel import select
from .routers import post,user, auth
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_password: str = "localhost"
    database_username: str = "postgres"
    secret_key: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"

settings = Settings()
print(settings.database_password)


SQLModel.metadata.create_all(engine)
app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def get_user(): #normal python function
    return {"message": "Hello World"} #this gets sent back to the user, also this a dictionary
#the dictionary is converted to json









