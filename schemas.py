from pydantic import BaseModel

class Task(BaseModel):
    id: int
    title: str
    description: str | None = None
    completed: bool = False