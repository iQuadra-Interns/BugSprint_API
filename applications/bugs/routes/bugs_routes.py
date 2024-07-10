from fastapi import APIRouter
from applications.bugs.utils.utils_bugs import fetch_bugs_list
from applications.bugs.rq_rs.rs_bugs import BugsListResponse , BugsList

router = APIRouter()

@router.get("/bugs_list", response_model=BugsListResponse)
def get_common_constants():
    constants = fetch_bugs_list()
    response_data = [BugsList(**row) for row in constants]
    return {"data": response_data}
