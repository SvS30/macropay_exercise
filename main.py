import uvicorn
from fastapi import FastAPI
from routes import api

app = FastAPI()

app.include_router(api.routes)

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)