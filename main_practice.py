import sys
import os
sys.path.append("/home/sanju/Documents/Intern_work/BugSprint_API")

os.environ['PYTHONDONTWRITEBYTECODE'] = '1'

from fastapi import FastAPI

from applications.bugs_list.routes.bugs_list_routes import router as bugs_list_router

from applications.common_constants.routes import all_route




app = FastAPI()
app.include_router(bugs_list_router, prefix="/api")
app.include_router(all_route.router, prefix="/api", tags=["common_constants"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
