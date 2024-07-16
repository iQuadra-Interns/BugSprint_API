from fastapi import FastAPI
from applications.common_constants.routes import common_constants_route

app = FastAPI()

app.include_router(common_constants_route.router, prefix="/api", tags=["common_constants"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
