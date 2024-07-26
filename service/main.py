import io
from typing import Annotated

import matplotlib.pyplot as plt
from fastapi import FastAPI, Depends
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.security import HTTPBasicCredentials, HTTPBasic

import service.Connector as Connector
from service.auth import get_current_username,security
import base64
import datetime

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/users/me")
def read_current_user(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    return {"username": credentials.username, "password": credentials.password}


@app.get("/graph")
async def get_graph():
    # Generate the graph
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [4, 5, 6])
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

    return StreamingResponse(buf, media_type="image/png")


@app.get("/graph2")
async def get_graph2():
    # Example data for the graph
    data = {
        "x": [1, 2, 3],
        "y": [4, 5, 6]
    }
    return JSONResponse(content=data)


@app.post("/checkTransection")
async def check_user():
    qurrey = f"SELECT * FROM TRANSECTION WHERE USER_ID = {user_id}"
    connector = Connector.Connector()

    result = connector.execute()
    return {'message': str(result)}
