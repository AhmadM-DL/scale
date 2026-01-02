from fastapi import FastAPI, HTTPException, Depends
from src.exceptions import ServiceException
from src.core_service import core_service
from src.config import APP_SECRET_KEY
from src.schema import PostRequest, EmptyResponse

from logging import getLogger
logger = getLogger(__name__)

app = FastAPI(title="AI LinkedIn Poster")

@app.post("/post", response_model=EmptyResponse)
def post_to_linkedin(request: PostRequest):
    if request.secret_key != APP_SECRET_KEY:
        raise HTTPException(status_code=401)
    try:
        core_service.post_to_linkedin()
        return EmptyResponse()
    except Exception as e:
        logger.error(f"Unexpected error in job execution: {e}")
        raise HTTPException(status_code=500)
