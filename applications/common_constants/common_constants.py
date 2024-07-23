import logging
import sys
sys.path.append("/mnt/python/lib")

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

from applications.common_constants.routes.all_route import router as common_constants_router

def add_routes(app: FastAPI):
    app.include_router(common_constants_router)


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


common_constants = configure_application()


@common_constants.get("/")
def _():
    resp = {
        'sts': True,
        'err': '',
        'msg': "You've reached the BUGS_LIST application. You need to access sub routes/resources/paths"
               " as /api/common_constants/*."
    }
    return resp