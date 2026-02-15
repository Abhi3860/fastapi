import time
from typing import Optional
from fastapi import FastAPI, Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg
from psycopg.rows import dict_row


app = FastAPI()

@app.get("/")
def get_user(): #normal python function
    return {"message": "Hello World"} #this gets sent back to the user, also this a dictionary
#the dictionary is converted to json

class Post(BaseModel):
    title: str
    content: str
    published: bool = True #defaults to 'true' if value is not provided

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

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data":posts}

def find_post(id):
    for p in my_posts:
        if p['id']==id:
            return p
        
def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p['id'] == id:
            return i


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute("""INSERT INTO posts (name, content, published) VALUES (%s,%s,%s) RETURNING *""", (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}

@app.get("/posts/{id}") #{id} is called a path parameter
def get_post(id: int, response: Response):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""",(str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message":f"Post with id {id} was not found"}
    
    return {
        "post detail": post
    }

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",(str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def create_post(id:int, post: Post):
    cursor.execute("""UPDATE posts SET name = %s, content=%s, published=%s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    return {"data": updated_post}

