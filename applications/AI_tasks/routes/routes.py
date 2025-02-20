from fastapi import APIRouter
from applications.AI_tasks.utils.ai_utils import rephrase_text
from applications.AI_tasks.rq_rs.ai_rq import RephraseRequest
from applications.AI_tasks.rq_rs.ai_rs import RephraseResponse

router = APIRouter()

@router.post("/rephrase", response_model=RephraseResponse)
def rephrase_api(request: RephraseRequest):

    rephrased_text = rephrase_text(request.description)
    return RephraseResponse(original=request.description, rephrased=rephrased_text)
