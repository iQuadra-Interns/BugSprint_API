from fastapi import APIRouter
from applications.ai_tasks.utils.ai_utils import rephrase_text
from applications.ai_tasks.rq_rs.ai_rq import RephraseRequest
from applications.ai_tasks.rq_rs.ai_rs import RephraseResponse

rephrase_description = APIRouter()

@rephrase_description.post("/rephrase", response_model=RephraseResponse)
def rephrase(request: RephraseRequest):
    rephrased_text = rephrase_text(request.description)
    return RephraseResponse(original=request.description, rephrased=rephrased_text)
