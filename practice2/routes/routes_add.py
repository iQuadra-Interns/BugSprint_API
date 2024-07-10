from fastapi import APIRouter, HTTPException
from practice2.utils.logic2_add import add_bug
from practice2.rq_rs.rq_add import AddBugRequest
from practice2.rq_rs.rs_add import AddBugResponse

router = APIRouter()

@router.post("/add_bug", response_model=AddBugResponse)
def create_bug(bug: AddBugRequest):
    result = add_bug(bug)
    if result["message"] == "Error adding bug":
        raise HTTPException(status_code=400, detail="Error adding bug")
    return result
