from os import getenv
from pymongo import MongoClient

def create_connection():
    mongo_client = MongoClient(getenv("DB_HOST", "localhost"), int(getenv("DB_PORT", 27017)))
    db_collection = mongo_client[str(getenv("DB_NAME", "test"))]
    return db_collection