import os
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'


from fastapi import FastAPI
from practice.routes.routes_bugs_list import router as bugs_list_router

app = FastAPI()

app.include_router(bugs_list_router, prefix="/api")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
