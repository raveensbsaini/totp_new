import typer
app = typer.Typer()
import httpx
@app.command()
def login():
    print(f"hello ")
    username = input("Enter your username :")
    password = input("Enter your password :")
    r =  httpx.post("https://localhost:8000/get_data",json={"username":username,"password":password})
    print(r,type(r),r.status_code)
@app.command()
def another_main(number:int):
    print(f"your age { number}")
if __name__ == "__main__":
    app()