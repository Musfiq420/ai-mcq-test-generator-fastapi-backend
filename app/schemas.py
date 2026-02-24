from typing import List

from pydantic import BaseModel, EmailStr, Field



# 1. Define the Schema for the Output (Pydantic)
class MCQOption(BaseModel):
    text: str = Field(description="The text of the option")
    isCorrect: bool = Field(description="Whether this option is the correct answer")

class MCQQuestion(BaseModel):
    question: str = Field(description="The question text")
    options: List[MCQOption] = Field(description="List of 4 options")
    explanation: str = Field(description="Explanation for the correct answer")

class MCQList(BaseModel):
    questions: List[MCQQuestion]

    

MCQ_JSON_SCHEMA = {
    "name": "mcq_list",
    "schema": {
        "type": "object",
        "properties": {
            "questions": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "question": {"type": "string"},
                        "options": {
                            "type": "array",
                            "minItems": 4,
                            "maxItems": 4,
                            "items": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "string"},
                                    "text": {"type": "string"},
                                    "isCorrect": {"type": "boolean"}
                                },
                                "required": ["id", "text", "isCorrect"]
                            }
                        },
                        "explanation": {"type": "string"}
                    },
                    "required": ["question", "options", "explanation"]
                }
            }
        },
        "required": ["questions"]
    }
}

