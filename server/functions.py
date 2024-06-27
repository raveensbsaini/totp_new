from databases import Database
import random
import asyncio
import hashlib
import secrets

database = Database("sqlite+aiosqlite:///database.db")
def make_hash(string:str):
    string = string.encode()
    hasher = hashlib.sha256(string)
    return hasher.hexdigest()    


async def set_otp(username,password,database):
    cookie = secrets.token_urlsafe(16)
    check = True
    while check:
        async with database.transaction():
            await database.execute("create table if not exists user( id integer primary key autoincrement, username text not null, password text not null, key blob default None,cookie text unique default None );")

            row = await database.fetch_one("select id from user where cookie =:cookie and username=:username and password =:password;",{"cookie":cookie,"username":username,"password":password})
            if row is None or  len(dict(row)) == 0:
                await database.execute("insert into user(username,password,cookie) values(:username,:password,:cookie)",{"username":username,"password":password,"cookie":make_hash(cookie)})
                check = False
                return cookie
            else:
                cookie = secrets.token_urlsafe(16)                    
                    
if __name__ == "__main__":
    print(asyncio.run(set_otp("ravindra kumar","saini",database)))