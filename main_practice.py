import sys
import os
from fastapi import FastAPI
import uvicorn

# Append the project path
sys.path.append("/home/sanju/Documents/Intern_work/BugSprint_API")

# Environment setup
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'

from applications.bugs_list.routes.bugs_list_routes import router as bugs_list_router

app = FastAPI()


# Create FastAPI instance


app = FastAPI()

app.include_router(bugs_list_router, prefix="/api")

# Root endpoint
@app.get("/")
def read_root():
    return {
        'sts': True,
        'err': '',
        'msg': "You've reached the BUGS_LIST application. Access sub routes/resources/paths like /api/bugs_list."
    }

# Run the application
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
