from fastapi import FastAPI
from applications.all.routes import all_route

app = FastAPI()

app.include_router(all_route.router, prefix="/api", tags=["common_constants"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
