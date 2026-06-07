from pydantic import BaseModel, Field
from typing import Optional


class Person(BaseModel):
    id: Optional[str] = None
    name: str = Field(min_length=3)
    number: str = Field(pattern=r"^\d{2,3}-\d{6,}$")