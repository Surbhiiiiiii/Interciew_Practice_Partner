from pydantic import BaseModel
from typing import List, Optional


class GenReq(BaseModel):
    role: str
    level: str
    last_answer: Optional[str] = ""


class NextReq(BaseModel):
    role: str
    question: str
    answer: str


class FeedbackReq(BaseModel):
    role: str
    level: str
    qa_pairs: List[dict]
