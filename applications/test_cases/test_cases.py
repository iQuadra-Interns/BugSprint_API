import sys

sys.path.append("/mnt/python/lib")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from applications.test_cases.routes.test_cases_routes import router as test_cases_router


def add_routes(app: FastAPI):
    app.include_router(test_cases_router)

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

test_cases_router = configure_application()

@test_cases_router.get("/test-cases")
def _():
    resp = {
        'sts': True,
        'err': '',
        'msg': "You've reached the test_cases application. You need to access sub routes/resources/paths"
               " as /api/test_cases/*."
    }
    return resp
