from fastapi import FastAPI
from practice2.routes.routes_add import router as add_bug_router

app = FastAPI()

app.include_router(add_bug_router, prefix="/api")
