from typing import Optional
from pydantic import BaseModel, Field


class Courses(BaseModel):
    id : Optional[int] = None
    name: str = Field(max_length=50,min_length=5)
    description: str = Field(max_length=500,min_length=10)
    lines_of_work: str = Field(max_length=500,min_length=5)
    specific_objetives: str = Field(max_length=500,min_length=15)
    type_of_course: str = Field(max_length=500,min_length=5)
    

    class Config:
        schema_extra = {
            "example":{
                 "name": "Diplomado en seguridad social",
                 "description": "Este diplomado permitira conocer y aplicar los preceptos normativos con una metodologia sencilla y pedagógica ",
                 "lines_of_work": "Se aborda el marco juridico y las politicas publicas que rigen el sistema de seguridad social en un pais determinado",
                 "specific_objetives":"proporcionar una información especializada en el ambito de seguridad social",
                 "type_of_course":"Academico" 
            }
        }