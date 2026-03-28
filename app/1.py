from fastapi import FastAPI
from .database import engine, get_db
from sqlmodel import SQLModel
from sqlmodel import select
from .routers import post,user, auth,vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

#SQLModel.metadata.create_all(engine)
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def get_user(): #normal python function
    return {"message": "Hello World"} #this gets sent back to the user, also this a dictionary
#the dictionary is converted to json









