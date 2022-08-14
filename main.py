import uvicorn
from fastapi import FastAPI
from routes import api
from os import getenv
from dotenv import load_dotenv

app = FastAPI()
load_dotenv(dotenv_path='./.env')
app.include_router(api.routes)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=getenv("APP_HOST", "localhost"),
        port=int(getenv("APP_PORT", 8000)),
        reload=True if getenv("APP_ENV") == 'local' else False
    )