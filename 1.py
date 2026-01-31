from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()

@app.get("/")
def get_user(): #normal python function
    return {"message": "Hello World"} #this gets sent back to the user, also this a dictionary
#the dictionary is converted to json

@app.get("/posts")
def get_posts():
    return {"data":"your posts"}

@app.post("/createposts")
def create_posts(payload: dict = Body(...)):
    print(payload)
    return {"message": "successfully created post"}
