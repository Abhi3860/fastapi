import time
from typing import Optional, List
from fastapi import FastAPI, Response,status,HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel

from random import randrange
import psycopg
from psycopg.rows import dict_row
from . import models, schemas, utils
from .database import engine, get_db
from sqlmodel import Session
from sqlmodel import SQLModel
from sqlmodel import select
from .routers import post,user



SQLModel.metadata.create_all(engine)
app = FastAPI()


app.include_router(post.router)
app.include_router(user.router)

@app.get("/")
def get_user(): #normal python function
    return {"message": "Hello World"} #this gets sent back to the user, also this a dictionary
#the dictionary is converted to json


while True:
    try:
        conn = psycopg.connect(host='localhost', dbname='fastapi', user='postgres', password='Hellrider3860', row_factory=dict_row)   
        cursor =conn.cursor()
        print("database connection successful")
        break
    except Exception as error:
        print("database connection failed")
        print("Error:", error)
        time.sleep(2)

my_posts = [{"title":"example post","content":"example content","id":1},{"title":"Food, Wonderful Food","Content":"Food is good","id":2}]




