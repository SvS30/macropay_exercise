import uvicorn
from fastapi import FastAPI
from routes.api import contact
from os import getenv
from dotenv import load_dotenv

app = FastAPI(
    title="Address Book Rest API",
    description="Macropay exercise on FastAPI",
    version="1.0.0"
)

load_dotenv(dotenv_path='./.env')
app.include_router(contact.routes)

@app.get('/')
def home():
    return { 'message': 'Hello World' }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=getenv("APP_HOST", "localhost"),
        port=int(getenv("APP_PORT", 8000)),
        reload=True if getenv("APP_ENV") == 'local' else False
    )