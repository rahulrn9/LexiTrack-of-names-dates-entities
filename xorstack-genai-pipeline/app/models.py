from pydantic import BaseModel
from typing import List, Optional

class TextPayload(BaseModel):
    text: str
    filename: Optional[str] = None

class ExtractionResponse(BaseModel):
    filename: str
    people: List[str]
    dates: List[str]
