from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from applications.bugs_list.routes.bugs_list_routes import router as bugs_list_router


def add_routes(app: FastAPI):
    app.include_router(bugs_list_router)


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


bugs_list_router = configure_application()


@bugs_list_router.get("/")
def _():
    resp = {
        'sts': True,
        'err': '',
        'msg': "You've reached the bugs_list application. You need to access sub routes/resources/paths"
               " as /api/bugs_list/*."
    }
    return resp
