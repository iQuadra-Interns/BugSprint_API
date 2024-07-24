
from fastapi import APIRouter
from applications.bugs_list.utils.utils_bugs_list import fetch_bugs_list
from applications.bugs_list.rq_rs.rs_bugs_list import BugsListResponse

router = APIRouter()

@router.post("/bugs_list", response_model=BugsListResponse)
def get_bugs_list():
    response = fetch_bugs_list()
    return response
