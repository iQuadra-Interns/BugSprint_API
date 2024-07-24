import sys
import os
import uvicorn
from fastapi import FastAPI
from fastapi.routing import Mount
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
import logging

# Ensure the applications are correctly imported

from applications.bugs_list.bugs_list import bugs_list_router
from applications.common_constants.common_constants import common_constants_router

# Configure logging
logging.basicConfig(
    filename="mainapp.log",
    format='%(asctime)s %(levelname)s %(module)s::%(filename)s:%(lineno)d::%(funcName)s %(message)s',
    level=logging.INFO
)
logger = logging.getLogger('bug-sprint-logger')

def add_applications():
    return [
        # Mount applications here
        
        Mount("/bugs_list", bugs_list_router),
        Mount("/common_constants", common_constants_router)
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

# Ensure individual handlers if needed

bugs_list_handler = Mangum(bugs_list_router)
common_constants_handler = Mangum(common_constants_router)

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
