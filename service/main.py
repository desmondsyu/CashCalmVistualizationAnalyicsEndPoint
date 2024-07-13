from typing import Annotated
import service.Security as Security
from fastapi import FastAPI, Depends
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import service.Class as Class
import matplotlib.pyplot as plt
import io
import service.Connector as Connector
import base64

app = FastAPI()
security = HTTPBasic()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/users/me")
def read_current_user(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    return {"username": credentials.username, "password": credentials.password}


@app.get("/hello/{name}")
async def say_hello(credentials: Annotated[HTTPBasicCredentials, Depends(security)],
                    name:str ):
    Security.get_current_username(credentials)
    return {"message": f"Hello {name}"}


@app.get("/graph")
async def get_graph(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
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
async def check_user(user_id: int):
    qurrey = f"SELECT * FROM TRANSECTION WHERE USER_ID = {user_id}"
    connector = Connector.Connector()

    result = connector.execute()
    return {'message': str(result)}
