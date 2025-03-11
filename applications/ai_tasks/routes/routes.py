from fastapi import APIRouter
from applications.ai_tasks.utils.ai_utils import rephrase_text
from applications.ai_tasks.rq_rs.ai_rq import RephraseRequest
from applications.ai_tasks.rq_rs.ai_rs import RephraseResponse
import logging
logger = logging.getLogger(__name__)
rephrase_description = APIRouter()


@rephrase_description.post("/rephrase", response_model=RephraseResponse, response_model_exclude_unset=True)
def rephrase(request: RephraseRequest) -> RephraseResponse:
        rephrased_response = rephrase_text(request.description)
        return rephrased_response

