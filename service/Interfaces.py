
from pydantic import BaseModel


class USER_INFO(BaseModel):
    username: str
    email: str
    password: str


class MONTH_SPENDING_INCOME(BaseModel):
    date: str
    month_spending: float
    month_income: float


class GROUP_SPENDING(BaseModel):
    date : str
    group_name: str
    amount: float
    type: str
class LABEL_SPENDING(BaseModel):
    date: str
    label_name: str
    amount: float

class SPENDING_ANALYSIS(BaseModel):
    current_spending: float
    expected_spending: float
    upper_bound_yellow_max: float
    max_bound_red_max: float
    percent_of_spending: float
class MESSAGE(BaseModel):
    message: str

