import logging
import sys

sys.path.append("/mnt/python/lib")
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from applications.AI_tasks.routes.routes import router

def add_routes(app: FastAPI):
    app.include_router(router)

def configure_application() -> FastAPI:
    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    add_routes(app)
    return app

rephrase_api_router = configure_application()

@rephrase_api_router.get("/")
def _():
    resp = {
        'sts': True,
        'err': '',
        'msg': "Welcome to the Description Rephrasing API! Access sub routes/resources/paths as /api/rephrase/*."
    }
    return resp
