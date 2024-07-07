from fastapi import FastAPI
from applications.signin.routes.signin_router import signin_router
app = FastAPI()
app.include_router(signin_router)

@app.get("/")
def greet():
    return "hello"