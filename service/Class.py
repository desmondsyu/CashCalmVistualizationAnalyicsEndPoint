from enum import Enum
from fastapi import FastAPI
from pydantic import BaseModel


class TransType(Enum):
    IN = 1
    EX = 2


class Transaction(BaseModel):
    user_id: int
    Amount: float
    Group: str
    Type: TransType


class User(BaseModel):
    user_id: int
    username: str
    password: str
