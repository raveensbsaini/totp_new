from databases import Database
import random
import asyncio
async def set_otp(username,password):
    cookie = str(random.randint(1000000,9999999))
    check = True
    while check:
        async with Database("sqlite+aiosqlite:///database.db") as database:
            async with database.transaction():
                row = await database.fetch_one("select id from user where cookie =:cookie and username=:username and password =:password;",{"cookie":cookie,"username":username,"password":password})
                row = dict(row)
                if len(row) == 0:
                    await database.execute("insert into user(username,password,cookie) values(:username,:password,:cookie)",{"username":username,"password":password,"cookie":cookie})
                    check = False
                    return cookie
                else:
                    cookie =str(random.randint(1000000,9999999))

            
if __name__ == "__main__":
    asyncio.run(set_otp("ravindra kumar","saini"))