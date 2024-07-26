from typing import Annotated
import service.Security as Security
from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import service.Class as Class
import matplotlib.pyplot as plt
import io
import service.Connector as Connector
import base64
import datetime

app = FastAPI()
security = HTTPBasic()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/users/me")
def read_current_user(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    return {"username": credentials.username, "password": credentials.password}


@app.get("/user_message")
async def say_hello(credentials: Annotated[HTTPBasicCredentials, Depends(security)],
                    name:str ):
    user_data = read_current_user(credentials)
    name = user_data["name"]
    date = datetime.date.today()

    return {"username": f"{name}",
            "date": f"{date}",
            "message": f"Hello {name}, you spending data to {date}"}

@app.get("/get_spending_analyst")
async def get_data(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    user_data = read_current_user(credentials)
    uname = user_data["username"]
    query = f"SELECT * FROM spend_data WHERE username = '{uname}'"

    connection = Connector.Connector()
    try :
        result = connection.execute(query)
        if result.rowcount == 0:
            return {"message": "No data found"}
    except Exception as e:
        return {"error message": str(e)}
    current_datetime = datetime.datetime.now()
    last_month = current_datetime - datetime.timedelta(days=30)
    query_current_spending = (f"SELECT SUM(AMOUNT) FROM spend_data WHERE username = '{uname}'"
                              f"AND TRAN_DATE > '{last_month}' and "
                              f"TRAN_DATE < '{current_datetime}'"
                              f"and TYPE is 'EX'")
    current_spending = connection.execute(query_current_spending)
    average_spending = current_spending.fetchone()[0]
    difference_spending = current_spending-average_spending



    data = {
        "current_montly_spend": f"{current_spending.fetchone()[0]}",
        "Average_Spending":f"{average_spending}",
        "Different_from_Average":f"{difference_spending}",
        "Upper_limit":f"{}",
        "Today Date":f"{datetime.date.today()}"
    }
    return JSONResponse(content=data)


@app.post("/checkTransection")
async def check_user(user_id: int):
    qurrey = f"SELECT * FROM TRANSECTION WHERE USER_ID = {user_id}"
    connector = Connector.Connector()

    result = connector.execute()
    return {'message': str(result)}
