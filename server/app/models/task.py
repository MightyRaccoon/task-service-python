from datetime import datetime
from typing import List

from pydantic import BaseModel


class TaskOut(BaseModel):
    task_id: int
    description: str
    tags: List[str]
    due_date: datetime


class TaskIn(BaseModel):
    description: str
    tags: List[str]
    due_date: datetime
