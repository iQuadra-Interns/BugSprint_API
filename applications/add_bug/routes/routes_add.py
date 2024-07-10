from fastapi import APIRouter, HTTPException
from applications.add_bug.utils.utils_add import add_bug
from applications.add_bug.rq_rs.rq_add import AddBugRequest
from applications.add_bug.rq_rs.rs_add import AddBugResponse

router = APIRouter()

@router.post("/add_bug", response_model=AddBugResponse)
def create_bug(bug: AddBugRequest):
    result = add_bug(bug)
    if result["message"] == "Error adding bug":
        raise HTTPException(status_code=400, detail="Error adding bug")
    return result
