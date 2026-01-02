from pydantic import BaseModel

class PostRequest(BaseModel):
    secret_key: str

class EmptyResponse(BaseModel):
    pass

