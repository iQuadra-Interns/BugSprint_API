import logging
from fastapi import APIRouter, HTTPException
from applications.bugs_list.utils.utils_bugs_list import fetch_bugs_list
from applications.bugs_list.rq_rs.rs_bugs_list import BugsListResponse

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/bugs_list", response_model=BugsListResponse)
def get_bugs_list():
    logger.info("Received request to fetch bugs list")
    try:
        response = fetch_bugs_list()
        return response
    except Exception as e:
        logger.error("Failed to fetch bugs list: %s", e)
        raise HTTPException(status_code=500, detail="Failed to fetch bugs list")
