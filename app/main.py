from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres',
                                password='236985T.q#$', cursor_factory=RealDictCursor)
        
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as err:
        print("Connecting to the database failed")


@app.get("/")
async def root():
    return {"message": "Hello World There!!!!!!"}


@app.get("/posts")
async def get_posts(): 
    cursor.execute(""" SELECT * FROM posts; """)
    my_posts = cursor.fetchall()
    return {"data": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_posts(post : Post):
    cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING  *; """, 
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()

    return {"data":new_post}
    


@app.get("/posts/{id}")
async def get_post(id: int):
    cursor.execute(""" SELECT * FROM posts WHERE id = %s; """, (str(id),))
    post = cursor.fetchone()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"Post with id:{id} not found")
    return {"post_detail": post}

@app.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING  *; """, str(id))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id:{id} does not exist")
    
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
async def update_post(id: int, post: Post):
    cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *;""",
                   (post.title, post.content, post.published, str(id)))
    updatedPost = cursor.fetchone()

    if not updatedPost:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id:{id} does not exist")
    
    conn.commit()
    return {"data": updatedPost}