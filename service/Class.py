from enum import Enum
from fastapi import FastAPI
from pydantic import BaseModel


class user_info(BaseModel):
    username: str
    email: str
    password: str

class current_monthly_spending(BaseModel):
    current_month_spending: float

class spending_analysis(BaseModel):
    current_spending: float
    expected_spending: float
    lower_bound_yellow_max: float
    upper_bound_red_max: float
    percent_of_spending: float