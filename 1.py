from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()

@app.get("/")
def get_user(): #normal python function
    return {"message": "Hello World"} #this gets sent back to the user, also this a dictionary
#the dictionary is converted to json

class Post(BaseModel):
    title: str
    content: str
    published: bool = True #defaults to 'true' if value is not provided
    rating: Optional[int] = None #fully optional field, defaults to 'none'


my_posts = [{"title":"example post","content":"example content","id":1},{"title":"Food, Wonderful Food","Content":"Food is good","id":2}]

@app.get("/posts")
def get_posts():
    return {"data":my_posts}



@app.post("/posts")
def create_posts(post: Post):
    post_dict = post.model_dump()
    post_dict['id']= randrange(0,10000000)
    my_posts.append(post_dict)
    return {"data": post_dict}
