from pydantic import BaseModel
from enum import Enum
class LLMResponseModel(BaseModel):
    explanation: str
    cost: float

    