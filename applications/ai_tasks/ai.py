from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from applications.ai_tasks.routes.routes import rephrase_description


def add_routes(app: FastAPI):
    app.include_router(rephrase_description)


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


ai_tasks_router = configure_application()


@ai_tasks_router.get("/")
def _():
    resp = {
        'sts': True,
        'err': '',
        'msg': "Welcome to the Description Rephrasing API! Access sub routes/resources/paths as /api/rephrase/*."
    }
    return resp
