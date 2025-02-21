
import sys

sys.path.append("/mnt/efs/BugSprint_312/lib/python3.12/site-packages")
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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