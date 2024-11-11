import logging
import sys

sys.path.append("/mnt/python/lib")

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

from applications.common_constants.routes.all_route import router as common_constants_router
from applications.common_constants.routes.forgot_password_router import forgot_password_router
from applications.common_constants.routes.reset_password_router import reset_password_router

def add_routes(app: FastAPI):
    app.include_router(common_constants_router)
    app.include_router(forgot_password_router)
    app.include_router(reset_password_router)


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


common_constants_router = configure_application()


@common_constants_router.get("/")
def _():
    resp = {
        'sts': True,
        'err': '',
        'msg': "You've reached the common_constants application. You need to access sub routes/resources/paths"

    }
    return resp
