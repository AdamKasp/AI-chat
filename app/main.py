from fastapi import FastAPI
from app.API.Agent.Agent import router as agent_router

app = FastAPI()

app.include_router(agent_router)

@app.get("/")
def read_root():
    return {"Hello": "World"}
