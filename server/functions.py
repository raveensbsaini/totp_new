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
            user = await database.fetch_one("select id from user where username=:username and password=:password;",{"username":username,"password":password})
            user = dict(user)
            user_id = user["id"]
            row = await database.fetch_one("select id from cookie where cookie=:cookie;",{"cookie":cookie})
            if row is None or  len(dict(row)) == 0:
                check = False
                return make_hash(cookie)
            else:
                cookie = secrets.token_urlsafe(16)                    
                    
if __name__ == "__main__":
    print(asyncio.run(set_otp("ravindra kumar","saini",database)))