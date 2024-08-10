from typing import Annotated
from fastapi import FastAPI, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBasicCredentials
from fastapi.middleware.cors import CORSMiddleware

import sys
import os

sys.path.append(os.path.expanduser(".."))

from service.auth import auth_username, security, auth_get_username_id
from service.ModelbaseOnEachUser import load_user_prediction, load_monthly_spending
import service.Class as Class

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


@app.get("/users/me",response_model=Class.user_info)
def read_current_user(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    data_encoded = jsonable_encoder(Class.user_info(username=auth_get_username_id(credentials)[0][1], email=credentials.username,
                                         password=credentials.password))
    return data_encoded


@app.get("/get-spending-data",response_model=dict)
async def get_spending_data(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    current_spending = load_monthly_spending(auth_get_username_id(credentials)[0][0])[0][0]
    data = Class.current_monthly_spending()
    if current_spending is None:
        data.current_month_spending = 0
    else:
        data.current_month_spending = current_spending
    data_encoded = jsonable_encoder(data)
    return data_encoded


@app.get("/get-spending-analysis",response_model=Class.spending_analysis)
async def get_spending_analysis(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    current_month_spending = load_monthly_spending(auth_get_username_id(credentials)[0][0])[0][0]
    user_id = auth_get_username_id(credentials)[0][0]
    if current_month_spending is None:
        current_month_spending = 0

    data = Class.spending_analysis()
    data.current_month_spending = float(current_month_spending)
    data.expected_spending = load_user_prediction(user_id)
    data.upper_limit_expected_spending = float(data.expected_spending * 1.25)
    data.max_limit_expected_spending = float(data.expected_spending * 1.5)
    data.percent_of_spending = round(current_month_spending * 100 / data.expected_spending, 1)

    data_encoded = jsonable_encoder(data)
    return data_encoded
