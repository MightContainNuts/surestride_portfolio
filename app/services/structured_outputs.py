from pydantic import BaseModel

class ValidQuery(BaseModel):
    is_valid_query: bool
    AI_response: str = None