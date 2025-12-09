from pydantic import BaseModel, Field
from typing import List

class Reflexion(BaseModel):
    missing: str = Field(description="critique of what is missing")
    superfluous: str = Field(description="critique of what is superfluous")

class AnswerQuestion(BaseModel):
    """Answer the question"""

    answer: str = Field(description="~250 word detailed answer to the question")
    reflexion: Reflexion = Field(description="your reflection on the initial answer")
    search_queries : List[str]= Field(description="1-3 search queries to improve the answer based on critique on current answer")


class RevisedAnswer(AnswerQuestion):
    """Revised your original answer to the question"""
    references: List[str] = Field(description="citation motivations to your updated answer.")