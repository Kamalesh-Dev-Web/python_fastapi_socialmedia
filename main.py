from typing import Optional
from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app=FastAPI()

class Post(BaseModel):
    title:str
    content: str   
    published:bool=True
    rating:Optional[int]=None
    
my_posts=[{"title":'title1',"content":'content1',"id":1},
          {"title":'title2',"content":'content2',"id":2}]

def find_post(id):
    for p in my_posts:
        if p["id"]==id:
            return p

@app.get('/')
def root():
    return{'data':'Hello folks welcome to social media fastAPI\'s API'}

@app.get('/posts')
def get_posts():
    return {'data':my_posts}

@app.post('/posts')
def create_post(post:Post):
    print(post)
    print(post.dict())
    post_dict=post.dict()
    post_dict["id"]=randrange(0,100000)
    my_posts.append(post_dict)
    return {'data':post_dict}

@app.get('/posts/{id}')
def get_post(id:int,response:Response):
    post=find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"the post with id {id} was not found")
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {"message":f"the post with id {id} was not found"}
    #return {"data":f"the post id is {id}"}
    return {"data":post}
