from pydantic import BaseModel
from datetime import datetime
from typing import Any
import enum


class Status(enum.Enum):
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"
    NOT_AUTHENTICATED = "NOT_AUTHENTICATED"
    ACCESS_DENIED = "ACCESS_DENIED"


class StatusResponse(BaseModel):
    status: Status = Status.ERROR
    completed: datetime

    def __init__(self, **data: Any):
        if "completed" not in data:
            data["completed"] = datetime.utcnow()
        super().__init__(**data)
