from pydantic import BaseModel
from typing import Optional

class Article(BaseModel):
    title: str
    date: str
    sub_title: Optional[str]
    content: str
    source: str # url

    def __str__(self):
        return f"{self.title}\n  {self.sub_title}\n {self.content}\n {self.date}"
