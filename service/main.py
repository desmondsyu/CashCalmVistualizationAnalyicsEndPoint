import decimal
from array import array
from datetime import datetime, timedelta
from typing import Annotated

import DateTime.DateTime
from fastapi import FastAPI, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
import json
from fastapi.responses import Response
from fastapi.security import HTTPBasicCredentials
from fastapi.middleware.cors import CORSMiddleware
from service.auth import auth_username, security, auth_get_username_id
from service.ModelbaseOnEachUser import load_user_prediction
import service.RecordSearching as RecordSearching
import service.Class as Class
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
    data_encoded = json.dumps(
        Class.USER_INFO(username=auth_get_username_id(credentials)[0][1], email=credentials.username,
                        password=credentials.password))
    response = Response(data_encoded)
    response.headers['Content-Type'] = 'application/json'
    response.headers['Cache-Control'] = 'private, max-age=3600'
    return response


@app.get("/get-spending-analysis", response_model=Class.SPENDING_ANALYSIS)
async def get_spending_analysis(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    current_month_spending = \
        RecordSearching.load_monthly_spending_or_income(auth_get_username_id(credentials)[0][0], datetime.today())[0]

    user_id = auth_get_username_id(credentials)[0][0]
    if current_month_spending is None:
        current_month_spending = float(0)
    expected_spending = float(load_user_prediction(user_id))

    data = Class.SPENDING_ANALYSIS(
        current_spending=current_month_spending,
        expected_spending=expected_spending,
        upper_bound_yellow_max=expected_spending * 1.25,
        max_bound_red_max=expected_spending * 1.5,
        percent_of_spending=round(current_month_spending / expected_spending, 1))
    data_encoded = jsonable_encoder(data)
    return data_encoded


# @app.get("/get-spending-break-down-in-one-month",response_model=list[Class.GROUP_AMOUNT])
# async def get_group_breakdown_data(credentials: Annotated[HTTPBasicCredentials, Depends(security)],Income: bool):
#     current_spending = RecordSearching.load_monthly_spending(auth_get_username_id(credentials)[0][0],datetime.today())[0][0]
#     data = Class.MONTH_SPENDING(year = datetime.today().year, )
#     data_encoded = jsonable_encoder(data)
#     return data_encoded


@app.get("/get-spending-data-in-range", response_model=list[Class.MONTH_SPENDING_INCOME])
async def get_spending_data(credentials: Annotated[HTTPBasicCredentials, Depends(security)],
                            from_year: int, from_month: int, to_year: int, to_month: int,
                            ):
    month_list = RecordSearching.moth_in_list_in_range(from_year, from_month, to_year, to_month)
    data = list()
    print(month_list)
    for month in month_list:
        spending_and_income = (RecordSearching.load_monthly_spending_or_income
                               (auth_get_username_id(credentials)[0][0], month))
        date_str = str(month.year) + '/' + str(month.month)
        result = Class.MONTH_SPENDING_INCOME(date=date_str, month_spending=spending_and_income[0]
                                      , month_income=spending_and_income[1] * -1)
        data.append(result.model_dump())
    data_encoded = json.dumps(data)
    response = Response(content=data_encoded, media_type="application/json")
    response.headers['Cache-Control'] = 'private, max-age=3600'
    return response
