import decimal
from array import array
from datetime import datetime, timedelta
from typing import Annotated, Union

import DateTime.DateTime
from fastapi import FastAPI, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
import json
from fastapi.responses import Response
from fastapi.security import HTTPBasicCredentials
from fastapi.middleware.cors import CORSMiddleware
from service.auth import *
from service.modelService import load_user_prediction
import service.connectorService as RecordSearching
import service.Interfaces as Class
import sys
import os

sys.path.append(os.path.expanduser(".."))

app = FastAPI(dependencies=[Depends(auth_username)])

# Configure CORS settings
origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Welcome!"}


@app.get("/users/me", response_model=Class.USER_INFO)
def read_current_user(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    data_encoded = Class.USER_INFO(username=auth_get_username_id(credentials)[0][1], email=credentials.username,
                                   password
                                   =credentials.password).model_dump()
    return data_encoded


@app.get("/spending/analysis", response_model=Class.SPENDING_ANALYSIS)
async def get_spending_analysis(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    current_month_spending = \
        RecordSearching.load_monthly_spending_or_income(auth_get_username_id(credentials)[0][0],
                                                        datetime.today())[0][1]

    user_id = auth_get_username_id(credentials)[0][0]
    if current_month_spending is None:
        current_month_spending = float(0)
    expected_spending = float(load_user_prediction(user_id))

    data = Class.SPENDING_ANALYSIS(
        current_spending=float(current_month_spending)*-1,
        expected_spending=round(expected_spending,2),
        upper_bound_yellow_max=round((expected_spending * 1.25),2),
        max_bound_red_max=round((expected_spending * 1.5),2),
        percent_of_spending=round(float(current_month_spending)*-100/ expected_spending, 2))
    return data


@app.get("/spending/income-expense/in-range", response_model=list[Class.MONTH_SPENDING_INCOME])
async def get_trend_data_income_and_expense(credentials: Annotated[HTTPBasicCredentials, Depends(security)],
                                            from_year: int, from_month: int, to_year: int, to_month: int,
                                            ):
    month_list = RecordSearching.moth_in_list_in_range(from_year, from_month, to_year, to_month)
    data = list()
    for month in month_list:
        spending_and_income = (RecordSearching.load_monthly_spending_or_income
                               (auth_get_username_id(credentials)[0][0], month))
        date_str = f"{month.year}/{month.month}"
        income = spending_and_income[0][0] if spending_and_income[0][0] is not None else 0.0
        expense = spending_and_income[0][1] if spending_and_income[0][1] is not None else 0.0
        result = Class.MONTH_SPENDING_INCOME(date=date_str, month_income=income
                                             , month_spending=expense * -1)
        data.append(result.model_dump())
    data_encoded = json.dumps(data)
    response = Response(content=data_encoded, media_type="application/json")
    response.headers['Cache-Control'] = 'private, max-age=20'
    return response


@app.get("/spending/transection-group/in-month/", response_model=list[Class.GROUP_SPENDING])
async def get_group_breakdown_data(credentials: Annotated[HTTPBasicCredentials, Depends(security)], month: int,
                                   year: int, return_in_type: bool):
    group_data = \
        RecordSearching.month_break_down_in_group(user_id=auth_get_username_id(credentials)[0][0], year=year,
                                                  month=month, in_type=return_in_type)
    if return_in_type:
        data = {"Income": [item.model_dump() for item in group_data[0]],
                "Expense": [item.model_dump() for item in group_data[1]]}
    else:
        data = [item.model_dump() for item in group_data]
    data_encoded = json.dumps(data)
    response = Response(content=data_encoded, media_type="application/json")
    return response


@app.get("/spending/transaction-group/in-range", response_model=list[Class.GROUP_SPENDING])
async def get_breakdown_trend_data_in_group(credentials: Annotated[HTTPBasicCredentials, Depends(security)],
                                            from_year: int, from_month: int, to_year: int, to_month: int):
    month_list = RecordSearching.moth_in_list_in_range(from_year, from_month, to_year, to_month)
    data = list()
    for month in month_list:
        month_data = RecordSearching.month_break_down_in_group(year=month.year, month=month.month,
                                                               user_id=auth_get_username_id(credentials)[0][0],
                                                               in_type=False)
        month_data_encoded = [item.model_dump() for item in month_data]
        data.extend(month_data_encoded)
    data_encoded = json.dumps(data)
    response = Response(content=data_encoded, media_type="application/json")
    response.headers['Cache-Control'] = 'private, max-age=20'
    return response


@app.get("/spending/lable/in-range", response_model=list[Class.LABEL_SPENDING])
async def get_breakdown_trend_data_in_label(credentials: Annotated[HTTPBasicCredentials, Depends(security)],
                                            from_year: int, from_month: int, to_year: int, to_month: int):
    month_list = RecordSearching.moth_in_list_in_range(from_year, from_month, to_year, to_month)
    data = list()
    for month in month_list:
        month_data = RecordSearching.month_breakdown_in_label(year=month.year, month=month.month,
                                                              user_id=auth_get_username_id(credentials)[0][0],
                                                              historical=False)
        month_data_encoded = [item.model_dump() for item in month_data]
        data.extend(month_data_encoded)
    data_encoded = json.dumps(data)
    response = Response(content=data_encoded, media_type="application/json")
    response.headers['Cache-Control'] = 'private, max-age=20'
    return response


@app.get("/spending/label/in-transaction-group", response_model=list[Class.GROUP_SPENDING])
async def get_group_spending_in_label(credentials: Annotated[HTTPBasicCredentials, Depends(security)], label_id: int):
    data = RecordSearching.label_break_down(auth_get_username_id(credentials)[0][0], label_id)
    data_encoded = [item.model_dump() for item in data]
    return data_encoded
