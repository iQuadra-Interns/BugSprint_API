import sys

sys.path.append("/mnt/python/lib")

import uvicorn
from fastapi import FastAPI
from fastapi.routing import Mount
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
import logging

from applications.admin.admin import admin
from applications.signin.signin import signin


logging.basicConfig(
    filename="mainapp.log",
    format='%(asctime)s %(levelname)s %(module)s::%(filename)s:%(lineno)d::%(funcName)s %(message)s',
    level=logging.INFO
)
logger = logging.getLogger('bug-sprint-logger')


def add_applications():
    return [
        Mount("applications/admin", admin),
        Mount("/signin", signin),
    ]


def configure_application() -> FastAPI:
    app = FastAPI(
        routes=add_applications(),
        title="Main application"
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app


application = configure_application()
application_handler = Mangum(application)

admin_handler = Mangum(admin)
signin_handler = Mangum(signin)


@application.get("/")
def main_app():
    resp = {
        'sts': False,
        'err': "IT'S A CRITICAL ERROR, IF YOU ARE SEEING THIS PAGE.",
        'msg': "You've reached main application of BugSprint. But you should not see this."
    }
    return resp


if __name__ == '__main__':
    uvicorn.run(application, host="127.0.0.1", port=8000)
