from fastapi import FastAPI, HTTPException,Cookie,Response
# adding this comment to make change try to make a pull request
from pydantic import BaseModel
from typing import Optional, Union 
from databases import Database
import httpx
import asyncio
""" /get_data 
expect username,password
if valid username, password:
return data(byte,base64)
   /post_data
except   username,password,key
if valid username,password:
    replace data with new data


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
async def get_data(username:str,new:Get):
    username = username
    database = Database('sqlite+aiosqlite:///database.db')
    await database.connect()
    rows = await database.fetch_one("select * from user where username=:username and password=:password;",{"username":username,"password":new.password})
    if rows is None:
        raise HTTPException(403,"No such username exits here")
    else:
        return dict(rows)["key"]
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
    