import sys

from applications.test_cases.test_cases import test_cases_router

sys.path.append("/mnt/efs/BugSprint_312/lib/python3.12/site-packages")

import uvicorn
from fastapi import FastAPI
from fastapi.routing import Mount
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
import logging

from applications.admin.admin import admin
from applications.signin.signin import signin
from applications.bugs.bugs import bugs
from applications.bugs_list.bugs_list import bugs_list_router
from applications.common_constants.common_constants import common_constants_router
from applications.ai_tasks.ai import ai_tasks_handler

# Configure logging
logging.basicConfig(
    filename="mainapp.log",
    format='%(asctime)s %(levelname)s %(module)s::%(filename)s:%(lineno)d::%(funcName)s %(message)s',
    level=logging.INFO
)
logger = logging.getLogger('bug-sprint-logger')


def add_applications():
    return [
        Mount("/bugs_list", bugs_list_router),
        Mount("/all_common_constants", common_constants_router),
        Mount("/admin", admin),
        Mount("/signin", signin),
        Mount("/bugs", bugs),
        Mount("/test_cases", test_cases_router),
        Mount("/ai_tasks", ai_tasks_handler)
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
bugs_handler = Mangum(bugs)
bug_search_handler = Mangum(bugs_list_router)
common_constants_handler = Mangum(common_constants_router)
ai_tasks_handler = Mangum(ai_tasks_handler)


@application.get("/")
def main_app():
    resp = {
        'sts': False,
        'err': "IT'S A CRITICAL ERROR, IF YOU ARE SEEING THIS PAGE.",
        'msg': "You've reached main application of BugSprint. But you should not see this."
    }
    return resp


if __name__ == '__main__':
    uvicorn.run(application, host="127.0.0.1", port=8001)
