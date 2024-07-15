from pymongo import MongoClient

from app.main import config

client = MongoClient(config.DATABASE_URL)
db = client.get_default_database()

def get_database():
    return db
