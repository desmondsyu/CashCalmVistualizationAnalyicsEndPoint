import io
from typing import Annotated

import matplotlib.pyplot as plt
from fastapi import FastAPI, Depends
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.security import HTTPBasicCredentials

import service.Connector as Connector
from service.auth import get_current_username,security

app = FastAPI(dependencies=[Depends(get_current_username())])


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/users/me")
def read_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    return {"username": credentials.username, "password": credentials.password}


@app.get("/graph")
async def get_graph():
    # Generate the graph
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [4, 5, 6])

    # Save the graph to a BytesIO object
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

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
