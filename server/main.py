from fastapi import FastAPI, HTTPException, Header,Request,Response
from contextlib import asynccontextmanager
from pydantic import BaseModel
from typing import AsyncContextManager, Optional, Union 
from databases import Database
import httpx
import asyncio
import random
import hashlib
from functions import set_otp,make_hash
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
    await database.execute("create table if not exists user( id integer primary key autoincrement, username text not null, password text not null, key blob default None) ;")

    await database.execute("create table if not exists cookie(id integer primary key autoincrement,user_id integer not null,cookie text not null);")
    yield
    await  database.disconnect()

    
app = FastAPI(lifespan=lifespan)
class Get(BaseModel):
    password:str
    
class Post(BaseModel):
    password:str
    key:bytes
class Get_cookie(BaseModel):
    cookie:str


@app.get("/")
async def root():
    return "welcome to the server made by ravindra kumar saini"






@app.post("/get_data/{username}")
async def get_data(username:str,new:Get,response:Response):
    password = new.password
    username = username
    async with database.transaction():
        
        row = await database.fetch_one("select * from user where username=:username and password=:password;",{"username":username,"password":password})
            
    if row is None:
        raise HTTPException(403,f"no username found {username}")
    else:
        row = dict(row)
        print("row",row)
        user_id  = row["id"]
        print("user_id " ,user_id)
        cookie = await set_otp(username,password,database)
        print("cookie",cookie)
        response.set_cookie(key="session_cookie",value=cookie,max_age=3600,domain="https://0.0.0.0:8001/index.html)")
        async with database.transaction():
            
            await database.execute("insert into cookie(user_id,cookie) values(:user_id,:cookie)",{"user_id":user_id,"cookie":cookie})
        return  row["key"]


# @app.post("/get_data_with_cookie")
# async def get_data_with_cookie(new1:Get_cookie):
#     cookie = new1.cookie;
#     async with database.transaction():
    
         
              
                   
                        
@app.post("/set_data/{username}")
async def set_data(new:Post,username:str):
    username = username
    database = Database("sqlite+aiosqlite:///database.db")
    await database.connect()
    # check if the username exits with its password then after do a change otherwise return httpsexception
    row = await database.fetch_one("select * from user where username=:username and password=:password",{"username":username,"password":new.password})
    print("row",row)
    if row is None:
        print(row == None)
        raise HTTPException(403,"no such username exits here")
    query = "UPDATE user SET key=:key where username=:username and password=:password;"
    values = {"username":username,"password":new.password,"key":new.key}   
    await database.execute(query=query,values=values)                 
    return "updated"
    