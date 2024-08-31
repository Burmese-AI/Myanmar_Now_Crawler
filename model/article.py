from pydantic import BaseModel
from datetime import date

class Article(BaseModel):
    title: str
    sub_title: str
    content: str
    date: date

    def __str__(self):
        return f"{self.title}\n  {self.sub_title}\n {self.content}\n {self.date}"
