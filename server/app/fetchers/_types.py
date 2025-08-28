from pydantic import BaseModel

class LLMResponseModel(BaseModel):
    explanation: str
    cost: float