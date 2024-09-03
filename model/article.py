from pydantic import BaseModel
from typing import Optional

class Article(BaseModel):
    title: str
    date: str
    subtitle: Optional[str]
    content: str
    source: str # url

    def __str__(self):
        return f"{self.title}\n  {self.subtitle}\n {self.content}\n {self.date}"
