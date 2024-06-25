from fastapi import FastAPI, HTTPException, Header,Request,Response
# adding this comment to make change try to make a pull request
from pydantic import BaseModel
from typing import Optional, Union 
from databases import Database
import httpx
import asyncio
import random
import hashlib
from functions import set_otp
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





    
users = {}
app = FastAPI()
class Get(BaseModel):
    password:str
    
class Post(BaseModel):
    password:str
    key:bytes



@app.get("/")
async def root():
    return "welcome to the server made by ravindra kumar saini"






@app.post("/get_data/{username}")
async def get_data(username:str,new:Get,response:Response):
    password = new.password
    username = username
    async with Database("sqlite+aiosqlite:///database.db") as database:
        async with database.transaction():
            row = await database.fetch_one("select key from user where username=:username and password=:password;",{"username":username,"password":password})
            row = dict(row)
            if row == 0:
                raise HTTPException(403,f"no username found {username}")
            else:
                response.set_cookie(key="cookie",value=await set_otp(username,password))
                return  row["key"]










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
    