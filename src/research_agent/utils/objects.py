from pydantic import BaseModel, Field
from typing import List, Optional


# Our Object Analyst
class Analyst(BaseModel):
    affilitation: str = Field(description="The affilitation of the analyst"),
    name: str = Field(description="The name of the analyst"),
    role: str = Field(description="The role of the analyst"),
    description: str = Field(description="The description of the analyst focus, concerns and motive"),

    @property
    def persona(self) -> str:
        return f"Name: {self.name}\n Role: {self.role}\n Affilitation: {self.affilitation}\n Description: {self.description}"

class Perspective(BaseModel):
    analysts: List[Analyst] = Field(description="Comprehensive list of analysts")


class SearchQuery(BaseModel):
    search_query: str = Field(description="Search query for the retrieval")
    


