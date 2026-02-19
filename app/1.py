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




SQLModel.metadata.create_all(engine)
app = FastAPI()




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

@app.get("/posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    #cursor.execute("""SELECT * FROM posts""")
    #posts = cursor.fetchall()

    posts = db.exec(select(models.Post)).all()

    return posts

def find_post(id):
    for p in my_posts:
        if p['id']==id:
            return p
        
def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p['id'] == id:
            return i


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    #cursor.execute("""INSERT INTO posts (name, content, published) VALUES (%s,%s,%s) RETURNING *""", (post.title, post.content, post.published))
    #new_post = cursor.fetchone()
    #conn.commit()
    new_post=models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)


    return new_post

@app.get("/posts/{id}", response_model=schemas.Post) #{id} is called a path parameter
def get_post(id: int, response: Response,db: Session = Depends(get_db)):
    #cursor.execute("""SELECT * FROM posts WHERE id = %s""",(str(id),))
    #post = cursor.fetchone()
    post = db.exec(select(models.Post).where(models.Post.id == id)).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message":f"Post with id {id} was not found"}
    
    return post

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    
    #cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",(str(id),))
    #deleted_post = cursor.fetchone()
    #conn.commit()
    deleted_post = db.exec(select(models.Post).where(models.Post.id == id))
    result = deleted_post.first()


    if result == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    db.delete(result)
    db.commit()


    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}", response_model=schemas.Post)
def create_post(id:int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    #cursor.execute("""UPDATE posts SET name = %s, content=%s, published=%s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    #updated_post = cursor.fetchone()
    #conn.commit()
    updated_post = db.exec(select(models.Post).where(models.Post.id == id)).first()
    u_post_data= post.model_dump(exclude_unset=True)

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    for key,value in u_post_data.items():
        setattr(updated_post, key, value)
    
    db.add(updated_post)
    db.commit()
    db.refresh(updated_post)



    return updated_post

@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    #hash the password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    
    new_user=models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)


    return new_user
