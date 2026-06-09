from fastapi import FastAPI

app = FastAPI()


@app.get("/", response_model=dict)
async def status():
    return {"message": "Conectado"}
