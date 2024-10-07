import logging
import sys

sys.path.append("/mnt/python/lib")

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

from applications.signin.routes.signin_router import signin_router


def add_routes(app: FastAPI):
    app.include_router(signin_router)


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


signin = configure_application()


@signin.get("/")
def _():
    resp = {
        'sts': True,
        'err': '',
        'msg': "You've reached the signin application. You need to access sub routes/resources/paths"
               " as /api/signin/*."
    }
    return resp