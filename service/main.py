import io
from typing import Annotated

import matplotlib.pyplot as plt
from fastapi import FastAPI, Depends
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.security import HTTPBasicCredentials, HTTPBasic

import service.Connector as Connector
import service.auth
from service.auth import auth_username, security, auth_get_use_id
from service.ModelbaseOnEachUser import load_user_prediction, load_monthly_sepnding
import base64
import datetime

app = FastAPI(dependencies=[Depends(auth_username)])


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/users/me")
def read_current_user(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    return {"username": credentials.username, "password": credentials.password}


@app.get("/get_spending_data")
async def get_spending_data(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    current_spending = load_monthly_sepnding(auth_get_use_id(credentials))[0][0]
    if current_spending is None:
        return {"message": "No spending data"}
    else:
        return {'this_month_spending': current_spending}


@app.get("/get_spending_analysis")
async def get_graph2(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    current_month_spending = load_monthly_sepnding(auth_get_use_id(credentials))[0][0]
    user_id = auth_get_use_id(credentials)
    if current_month_spending is None:
        current_month_spending = 0
    else:
        current_month_spending = float(current_month_spending)
    expected_spending = load_user_prediction(user_id)
    upper_limit_expected_spending = float(expected_spending * 1.25)
    max_limit_expected_spending = float(expected_spending * 1.5)
    percent_of_spending = round(current_month_spending * 100/ expected_spending,1)
    data = {
        'current_spending': current_month_spending,
        'expected_spending': expected_spending,
        'lower_bound_yellow_max': upper_limit_expected_spending,
        'upper_bound_red_max': max_limit_expected_spending,
        'percent_of_spending': f"{percent_of_spending}%"
    }
    return data
