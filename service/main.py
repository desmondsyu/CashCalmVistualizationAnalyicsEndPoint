from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.responses import JSONResponse
import Class
import matplotlib.pyplot as plt
import io

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

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

@app.post("/addTransection")
async def addTransection(trans : Class.Transaction):
    #....Code to add Transection To DB
    return {'message':'Transection added'}