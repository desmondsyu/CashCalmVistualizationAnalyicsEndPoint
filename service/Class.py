from enum import Enum
from fastapi import FastAPI
from pydantic import BaseModel
from service.main import app


class TransType(Enum):
    IN = 1
    EX = 2


class Transaction(BaseModel):
    user_id: int
    Amount: float
    Group: str
    Type: TransType

