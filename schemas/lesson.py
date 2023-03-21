from typing import Optional
from pydantic import BaseModel, Field
from fastapi import File

class Lesson(BaseModel):
    id: Optional[int] = None
    name: str = Field(max_length=100, min_length=10)
    description: str = Field(max_length=1000, min_length=10)
    title_resource: str = Field(max_length=100, min_length=10)

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "name": "Lesson 1",
                "description": "Lesson 1 description",
                "title_resource": "lectura 1",
            }
        }