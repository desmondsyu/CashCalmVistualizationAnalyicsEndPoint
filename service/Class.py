from enum import Enum
from fastapi import FastAPI
from pydantic import BaseModel


class TransType(Enum):
    IN = 1
    EX = 2
