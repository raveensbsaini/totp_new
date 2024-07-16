from logging import raiseExceptions
from fastapi import FastAPI, HTTPException, Header,Request,Response
from contextlib import asynccontextmanager
from pydantic import BaseModel
from typing import AsyncContextManager, Optional, Union 
from databases import Database
import httpx
import asyncio
import random
import hashlib
from fastapi.middleware.cors import CORSMiddleware
from functions import set_otp,make_hash

from fastapi.staticfiles import StaticFiles

""" /get_data 
expect username,password
if valid username, password:
return data(byte,base64)
   /post_data
except   username,password,key
if valid username,password:
    replace data with new data
=====

"""
database = Database("sqlite+aiosqlite:///database.db")
@asynccontextmanager
async def lifespan(app:FastAPI):
    await database.connect()
    await database.execute("create table if not exists user( id integer primary key autoincrement,username text not null, password text not null,recovery_key text default None, key text default None) ;")

    await database.execute("create table if not exists cookies(id integer primary key autoincrement,user_id integer not null,cookie text not null);")
    yield
    await  database.disconnect()
    
app = FastAPI(lifespan=lifespan)


origins = [
    "http://localhost:8001"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class Get(BaseModel):
    password:str
    
class Post(BaseModel):
    password:str
    key:str
class Get_cookie(BaseModel):
    cookie:str


class Sign(BaseModel):
    password:str
    recovery_key:str

@app.get("/api")
async def root():
    return "welcome to the server made by ravindra kumar saini"


@app.post("/api/get_data/{username}")
# assumption here this route is only used for login puropse only
async def get_data(username:str,new:Get,response:Response):
    password = new.password
    username = username
    print("username",username)
    print("password",password)
        
    row = await database.fetch_one("select id from user where username=:username and password=:password;",{"username":username,"password":password})            
    print("row",row)
    if row is None:
        raise HTTPException(403,f"no username found {username}")
    else:
        row = dict(row)
        user_id  = row["id"]
        cookie = await set_otp(username,password,database)
        response.set_cookie(key="session_cookie",value=cookie,max_age=3600)
        async with database.transaction():
            
            await database.execute("insert into cookies(user_id,cookie) values(:user_id,:cookie)",{"user_id":user_id,"cookie":cookie})
        return  {"message":"send successfull cookie"}


@app.post("/cookie")
async def get_data_with_cookie(new1:Get_cookie): #     cookie = new1.cookie;
    cookie = new1.cookie;
    row = await database.fetch_one("select user_id from cookies where cookie = :cookie;",{"cookie":cookie});
    if row is None:
        raise HTTPException(403,"no such cookie found.")
    else:
        row = dict(row)
        user_id = row["user_id"]
        row = await database.fetch_one("select * from user where id=:id;",{"id":user_id})
        if row is None:
            raise HTTPException(403,"no such user found");
        else:
            row = dict(row)
            key = row["key"]
            print("key",key)
        return row
        
    







@app.get("/s")
async def signup3():
    ...

@app.post("/s")
async def signup2():
    ...


@app.post("/signup/")
async def signup1(username:str,sign:Sign,reponse:Response):
    ...

    
@app.post("/signup/{username}")
async def signup(username:str,sign:Sign,reponse:Response):
    password = sign.password
    recovery_key = sign.recovery_key
    row = await database.fetch_one("select id from user where username=:username ;",{"username":username })
    if row is None :
        async with database.transaction():
            await database.execute("insert into user(username,password,recovery_key) values(:username,:password,:recovery_key)",{"username":username,"password":password,"recovery_key":recovery_key})
            user_id = await database.fetch_one("select id from user where username = :username and password = :password",{"username":username,"password":password})
            print(user_id,type(user_id))
            user_id = dict(user_id)
            user_id = user_id["id"]
            print("user_id ",user_id)
            cookie = await set_otp(username,password,database)
            await database.execute("insert into cookies(user_id,cookie) values(:user_id,:cookie)",{"user_id":user_id,"cookie":cookie})
            reponse.set_cookie(key="session_cookie",value=cookie,max_age=3600)
            return {"message":"signup succesfully"}
        
    else:
        raise HTTPException(403,f"{username} alread exists try with another username")
@app.post("/set_data/{username}")
async def set_data(username:str,new:Post):
    password = new.password
    key = new.key
    row = await database.fetch_one("select * from user where username=:username and password=:password;",{"username":username,"password":password})
    if row is None:
        raise HTTPException(403,"either username or password is incorrect")
    else:
        row = dict(row)
        id = row["id"]
        async with database.transaction():
            await database.execute("update user set key =:new_key where id =:id;",{"new_key":key,"id":id})
        return "success"

app.mount("/", StaticFiles(directory="static", html=True), name="static")
