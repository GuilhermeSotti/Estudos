from pydantic import BaseModel
from typing import List

class YieldRequest(BaseModel):
    features: List[float]

class LossRequest(BaseModel):
    features: List[float]
