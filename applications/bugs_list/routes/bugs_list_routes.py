from fastapi import APIRouter
from applications.bugs_list.utils.utils_bugs_list import fetch_bugs_list
from applications.bugs_list.rq_rs.rs_bugs_list import BugsListResponse, BugsList

router = APIRouter()

@router.post("/bugs_list", response_model=BugsListResponse)
def get_common_constants():
    constants = fetch_bugs_list()
    response_data = [BugsList(**row) for row in constants]
    return {"data": response_data}
